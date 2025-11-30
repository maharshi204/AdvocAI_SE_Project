"""
Model Management Module
Handles downloading and loading of the embedding model
"""

import os
from pathlib import Path
from typing import Optional
from sentence_transformers import SentenceTransformer

from ..config import RAGConfig
from ..utils import logger


class EmbeddingModelManager:
    """
    Manages the embedding model lifecycle:
    - Downloading
    - Caching
    - Loading
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize model manager.
        
        Args:
            model_name: Name of the model (defaults to config)
        """
        self.model_name = model_name or RAGConfig.EMBEDDING_MODEL_NAME
        self.model = None
        self.cache_dir = RAGConfig.MODEL_CACHE_DIR
        
    def is_model_cached(self) -> bool:
        """
        Check if model is already downloaded and cached.
        
        Returns:
            True if model exists in cache
        """
        # sentence-transformers uses a specific cache structure
        model_path = self.cache_dir / self.model_name.replace("/", "_")
        return model_path.exists()
    
    def download_model(self, force: bool = False) -> bool:
        """
        Download the embedding model.
        
        Args:
            force: Force re-download even if cached
            
        Returns:
            True if successful
        """
        try:
            if self.is_model_cached() and not force:
                logger.info(f"Model '{self.model_name}' already cached")
                return True
            
            logger.info(f"Downloading model: {self.model_name}")
            logger.info(f"This may take a few minutes (~80MB download)...")
            
            # This will automatically download the model
            model = SentenceTransformer(
                self.model_name,
                device=RAGConfig.DEVICE,
                cache_folder=str(self.cache_dir)
            )
            
            logger.info(f"✅ Model downloaded successfully!")
            logger.info(f"📁 Cached at: {self.cache_dir}")
            logger.info(f"📊 Vector dimension: {model.get_sentence_embedding_dimension()}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to download model: {str(e)}")
            return False
    
    def load_model(self) -> SentenceTransformer:
        """
        Load the embedding model into memory.
        
        Returns:
            Loaded SentenceTransformer model
        """
        if self.model is not None:
            logger.debug("Model already loaded, returning cached instance")
            return self.model
        
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            self.model = SentenceTransformer(
                self.model_name,
                device=RAGConfig.DEVICE,
                cache_folder=str(self.cache_dir)
            )
            
            logger.info(f"✅ Model loaded successfully on device: {RAGConfig.DEVICE}")
            return self.model
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        if self.model is None:
            self.load_model()
        
        return {
            'model_name': self.model_name,
            'vector_dimension': self.model.get_sentence_embedding_dimension(),
            'max_seq_length': self.model.max_seq_length,
            'device': str(self.model.device),
            'cached': self.is_model_cached()
        }


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage embedding model")
    parser.add_argument('--download', action='store_true', help='Download the model')
    parser.add_argument('--info', action='store_true', help='Show model information')
    parser.add_argument('--force', action='store_true', help='Force re-download')
    
    args = parser.parse_args()
    
    manager = EmbeddingModelManager()
    
    if args.download:
        manager.download_model(force=args.force)
    
    if args.info:
        info = manager.get_model_info()
        print("\nModel Information:")
        print("=" * 40)
        for key, value in info.items():
            print(f"{key:20}: {value}")
        print("=" * 40)
