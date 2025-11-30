"""
File 3: Query Processor
Processes user queries and converts them to embeddings
"""

import re
from typing import Dict, Any, Optional, List
import numpy as np

from .config import RAGConfig
from .models.download_model import EmbeddingModelManager
from .utils import logger, clean_text


class QueryProcessor:
    """
    Processes user queries for template retrieval.
    Handles query preprocessing, embedding generation, and filter extraction.
    """
    
    def __init__(self):
        """Initialize the query processor."""
        self.model_manager = EmbeddingModelManager()
        self.model = None
        
        logger.info("Initialized QueryProcessor")
    
    def initialize(self):
        """Load the embedding model."""
        if self.model is None:
            logger.info("Loading embedding model for query processing...")
            self.model = self.model_manager.load_model()
            logger.info("✅ Model loaded")
    
    def preprocess_query(self, query: str) -> str:
        """
        Clean and normalize the query text.
        
        Args:
            query: Raw query string
            
        Returns:
            Preprocessed query string
        """
        # Basic cleaning
        query = clean_text(query)
        
        # Convert to lowercase for processing
        query_lower = query.lower()
        
        # Remove special characters but keep important ones
        query_lower = re.sub(r'[^\w\s\-]', ' ', query_lower)
        
        # Remove extra whitespace
        query_lower = ' '.join(query_lower.split())
        
        return query_lower
    
    def extract_filters_from_query(self, query: str) -> Dict[str, Any]:
        """
        Extract potential filters from the query.
        Looks for category or document type keywords.
        
        Args:
            query: Query string
            
        Returns:
            Dictionary of filters to apply
        """
        filters = {}
        query_lower = query.lower()
        
        # Common legal document categories
        category_keywords = {
            'employment': ['employment', 'employee', 'work agreement', 'job contract'],
            'nda': ['nda', 'non-disclosure', 'confidentiality', 'non disclosure'],
            'service': ['service agreement', 'service contract', 'consulting'],
            'business': ['business', 'partnership', 'joint venture'],
            'lease': ['lease', 'rental', 'property'],
            'sale': ['purchase', 'sale', 'buy', 'sell'],
            'license': ['license', 'licensing'],
            'contract': ['contract', 'agreement']
        }
        
        # Check for category matches
        detected_categories = []            
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_categories.append(category)
        
        if detected_categories:
            filters['detected_categories'] = detected_categories
            logger.debug(f"Detected categories: {detected_categories}")
        
        return filters
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Convert query to embedding vector.
        
        Args:
            query: Query string
            
        Returns:
            Embedding vector as NumPy array
        """
        if self.model is None:
            self.initialize()
        
        try:
            embedding = self.model.encode(
                [query],
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embedding[0]  # Return first (and only) embedding
            
        except Exception as e:
            logger.error(f"Failed to embed query: {str(e)}")
            raise
    
    def process_query(self, query: str, extract_filters: bool = True) -> Dict[str, Any]:
        """
        Main method to process a query.
        
        Args:
            query: Raw query string
            extract_filters: Whether to extract filters from query
            
        Returns:
            Dictionary with processed query data
        """
        logger.info(f"Processing query: '{query}'")
        
        # Preprocess
        preprocessed_query = self.preprocess_query(query)
        logger.debug(f"Preprocessed: '{preprocessed_query}'")
        
        # Extract filters if requested
        filters = {}
        if extract_filters:
            filters = self.extract_filters_from_query(query)
        
        # Generate embedding
        query_vector = self.embed_query(preprocessed_query)
        
        result = {
            'original_query': query,
            'preprocessed_query': preprocessed_query,
            'query_vector': query_vector,
            'filters': filters,
            'vector_dimension': len(query_vector)
        }
        
        logger.info(f"✅ Query processed (vector dim: {result['vector_dimension']})")
        return result
    
    def process_batch_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple queries at once.
        
        Args:
            queries: List of query strings
            
        Returns:
            List of processed query dictionaries
        """
        logger.info(f"Processing {len(queries)} queries...")
        
        results = []
        for query in queries:
            try:
                result = self.process_query(query)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process query '{query}': {str(e)}")
                results.append(None)
        
        logger.info(f"✅ Processed {len([r for r in results if r])} queries successfully")
        return results


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process queries")
    parser.add_argument('query', type=str, help='Query string to process')
    parser.add_argument('--no-filters', action='store_true', help='Disable filter extraction')
    
    args = parser.parse_args()
    
    processor = QueryProcessor()
    result = processor.process_query(args.query, extract_filters=not args.no_filters)
    
    print("\nQuery Processing Result:")
    print("=" * 60)
    print(f"Original Query: {result['original_query']}")
    print(f"Preprocessed:   {result['preprocessed_query']}")
    print(f"Vector Dim:     {result['vector_dimension']}")
    print(f"Filters:        {result['filters']}")
    print("=" * 60)
