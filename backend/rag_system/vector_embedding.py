"""
File 2: Vector Embedding Pipeline
Generates embeddings for text chunks and stores them in Qdrant
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from .config import RAGConfig
from .models.download_model import EmbeddingModelManager
from .utils import logger, load_json, save_json, format_timestamp


class VectorEmbeddingPipeline:
    """
    Pipeline for generating embeddings and storing in Qdrant vector database.
    """
    
    def __init__(self):
        """Initialize the vector embedding pipeline."""
        self.model_manager = EmbeddingModelManager()
        self.model = None
        self.qdrant_client = None
        self.collection_name = RAGConfig.COLLECTION_NAME
        
        logger.info("Initialized VectorEmbeddingPipeline")
    
    def initialize(self):
        """Initialize model and Qdrant client."""
        # Load embedding model
        logger.info("Loading embedding model...")
        self.model = self.model_manager.load_model()
        
        # Initialize Qdrant client
        logger.info(f"Connecting to Qdrant ({RAGConfig.QDRANT_MODE} mode)...")
        self.qdrant_client = RAGConfig.get_qdrant_client()
        
        logger.info("✅ Initialization complete")
    
    def create_collection(self, recreate: bool = False):
        """
        Create Qdrant collection for storing vectors.
        
        Args:
            recreate: If True, delete existing collection and create new one
        """
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_exists = any(c.name == self.collection_name for c in collections)
            
            if collection_exists:
                if recreate:
                    logger.info(f"Deleting existing collection: {self.collection_name}")
                    self.qdrant_client.delete_collection(self.collection_name)
                else:
                    logger.info(f"Collection '{self.collection_name}' already exists")
                    return
            
            # Create new collection
            logger.info(f"Creating collection: {self.collection_name}")
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=RAGConfig.VECTOR_DIM,
                    distance=Distance.COSINE
                )
            )
            
            logger.info(f"✅ Collection '{self.collection_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            NumPy array of embeddings
        """
        if not texts:
            return np.array([])
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=RAGConfig.EMBEDDING_BATCH_SIZE,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise
    
    def load_processed_documents(self) -> List[Dict[str, Any]]:
        """
        Load all processed documents from disk.
        
        Returns:
            List of processed document dictionaries
        """
        processed_dir = RAGConfig.PROCESSED_DATA_DIR
        
        if not processed_dir.exists():
            logger.error(f"Processed data directory not found: {processed_dir}")
            return []
        
        documents = []
        json_files = list(processed_dir.glob("*.json"))
        
        logger.info(f"Loading {len(json_files)} processed documents...")
        
        for json_file in json_files:
            try:
                doc_data = load_json(str(json_file))
                documents.append(doc_data)
            except Exception as e:
                logger.warning(f"Failed to load {json_file}: {str(e)}")
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def prepare_points_for_upload(self, documents: List[Dict[str, Any]]) -> List[PointStruct]:
        """
        Prepare document chunks as Qdrant points with embeddings.
        
        Args:
            documents: List of processed documents
            
        Returns:
            List of PointStruct objects ready for upload
        """
        all_points = []
        all_texts = []
        all_metadata = []
        
        logger.info("Preparing chunks for embedding...")
        
        # Collect all chunks and their metadata
        for doc in documents:
            doc_metadata = doc['metadata']
            
            for chunk in doc['chunks']:
                chunk_text = chunk['text']
                
                # Create metadata for this chunk
                chunk_metadata = {
                    'doc_id': doc['doc_id'],
                    'chunk_index': chunk['chunk_index'],
                    'filename': doc_metadata['filename'],
                    'file_path': doc_metadata['file_path'],
                    'category': doc_metadata['category'],
                    'subcategory': doc_metadata.get('subcategory', ''),
                    'hierarchy': doc_metadata['hierarchy'],
                    'chunk_text': chunk_text[:500],  # Store preview of text
                    'full_text_length': chunk['length']
                }
                
                all_texts.append(chunk_text)
                all_metadata.append(chunk_metadata)
        
        logger.info(f"Total chunks to embed: {len(all_texts)}")
        
        # Generate embeddings in batches
        logger.info("Generating embeddings...")
        all_embeddings = []
        
        batch_size = RAGConfig.EMBEDDING_BATCH_SIZE
        num_batches = (len(all_texts) + batch_size - 1) // batch_size
        
        iterator = tqdm(range(num_batches), desc="Embedding batches") if RAGConfig.SHOW_PROGRESS else range(num_batches)
        
        for i in iterator:
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(all_texts))
            batch_texts = all_texts[start_idx:end_idx]
            
            batch_embeddings = self.generate_embeddings(batch_texts)
            all_embeddings.append(batch_embeddings)
        
        all_embeddings = np.vstack(all_embeddings)
        
        logger.info(f"Generated {len(all_embeddings)} embeddings")
        
        # Create PointStruct objects
        logger.info("Creating Qdrant points...")
        for i, (embedding, metadata) in enumerate(zip(all_embeddings, all_metadata)):
            point = PointStruct(
                id=str(uuid.uuid4()),  # Generate unique ID
                vector=embedding.tolist(),
                payload=metadata
            )
            all_points.append(point)
        
        logger.info(f"Created {len(all_points)} points")
        return all_points
    
    def upload_to_qdrant(self, points: List[PointStruct], batch_size: int = 100):
        """
        Upload points to Qdrant collection in batches.
        
        Args:
            points: List of PointStruct objects
            batch_size: Number of points to upload per batch
        """
        logger.info(f"Uploading {len(points)} points to Qdrant...")
        
        num_batches = (len(points) + batch_size - 1) // batch_size
        
        iterator = tqdm(range(num_batches), desc="Uploading to Qdrant") if RAGConfig.SHOW_PROGRESS else range(num_batches)
        
        for i in iterator:
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(points))
            batch_points = points[start_idx:end_idx]
            
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch_points
            )
        
        logger.info("✅ Upload complete")
    
    def embed_and_store(self, recreate_collection: bool = False) -> Dict[str, Any]:
        """
        Main method to embed all documents and store in Qdrant.
        
        Args:
            recreate_collection: Whether to recreate the collection
            
        Returns:
            Statistics dictionary
        """
        logger.info("=" * 60)
        logger.info("Starting Vector Embedding Pipeline")
        logger.info("=" * 60)
        
        # Initialize
        self.initialize()
        
        # Create collection
        self.create_collection(recreate=recreate_collection)
        
        # Load processed documents
        documents = self.load_processed_documents()
        
        if not documents:
            logger.error("No processed documents found! Run ingestion first.")
            return {'success': False, 'message': 'No documents to embed'}
        
        # Prepare points with embeddings
        points = self.prepare_points_for_upload(documents)
        
        # Upload to Qdrant
        self.upload_to_qdrant(points)
        
        # Get collection info
        collection_info = self.qdrant_client.get_collection(self.collection_name)
        
        stats = {
            'success': True,
            'num_documents': len(documents),
            'num_vectors': len(points),
            'collection_name': self.collection_name,
            'vector_dimension': RAGConfig.VECTOR_DIM,
            'model_name': RAGConfig.EMBEDDING_MODEL_NAME,
            'qdrant_mode': RAGConfig.QDRANT_MODE,
            'points_count': collection_info.points_count,
            'embedded_at': format_timestamp()
        }
        
        # Save stats
        stats_file = RAGConfig.METADATA_DIR / "embedding_stats.json"
        save_json(stats, str(stats_file))
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("Embedding Complete!")
        logger.info("=" * 60)
        logger.info(f"✅ Embedded {stats['num_documents']} documents")
        logger.info(f"📊 Total vectors: {stats['num_vectors']}")
        logger.info(f"🗄️  Collection: {stats['collection_name']}")
        logger.info(f"📏 Vector dimension: {stats['vector_dimension']}")
        logger.info(f"🤖 Model: {stats['model_name']}")
        logger.info("=" * 60)
        
        return stats
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Qdrant collection.
        
        Returns:
            Dictionary with collection statistics
        """
        if self.qdrant_client is None:
            self.qdrant_client = RAGConfig.get_qdrant_client()
        
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            
            return {
                'collection_name': self.collection_name,
                'points_count': collection_info.points_count,
                'vector_dimension': collection_info.config.params.vectors.size,
                'distance_metric': collection_info.config.params.vectors.distance.name
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate and store embeddings")
    parser.add_argument('--recreate', action='store_true', help='Recreate collection')
    parser.add_argument('--stats', action='store_true', help='Show collection statistics')
    
    args = parser.parse_args()
    
    pipeline = VectorEmbeddingPipeline()
    
    if args.stats:
        pipeline.qdrant_client = RAGConfig.get_qdrant_client()
        stats = pipeline.get_collection_stats()
        print("\nCollection Statistics:")
        print("=" * 40)
        for key, value in stats.items():
            print(f"{key:20}: {value}")
        print("=" * 40)
    else:
        stats = pipeline.embed_and_store(recreate_collection=args.recreate)
        print(f"\n✅ Success: {stats['success']}")
