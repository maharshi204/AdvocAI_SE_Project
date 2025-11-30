"""
File 4: Template Retrieval
Searches vector database and retrieves relevant templates
"""

from typing import List, Dict, Any, Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue

from .config import RAGConfig
from .query_processor import QueryProcessor
from .utils import logger


class TemplateRetriever:
    """
    Retrieves relevant templates from the vector database.
    Handles similarity search, filtering, and result ranking.
    """
    
    def __init__(self):
        """Initialize the template retriever."""
        self.qdrant_client = None
        self.query_processor = QueryProcessor()
        self.collection_name = RAGConfig.COLLECTION_NAME
        
        logger.info("Initialized TemplateRetriever")
    
    def initialize(self):
        """Initialize Qdrant client and query processor."""
        if self.qdrant_client is None:
            logger.info("Connecting to Qdrant...")
            self.qdrant_client = RAGConfig.get_qdrant_client()
            logger.info("✅ Connected to Qdrant")
        
        self.query_processor.initialize()
    
    def search_similar(
        self, 
        query_vector: List[float], 
        top_k: int = None,
        score_threshold: float = None,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            category_filter: Filter by specific category
            
        Returns:
            List of search results with scores and metadata
        """
        if self.qdrant_client is None:
            self.initialize()
        
        top_k = top_k or RAGConfig.TOP_K_RESULTS
        score_threshold = score_threshold or RAGConfig.MIN_SIMILARITY_SCORE
        
        # Build filter if category specified
        query_filter = None
        if category_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )
        
        try:
            # Perform search
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k * 2,  # Get more results for filtering
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True
            )
            
            logger.info(f"Found {len(search_results)} results above threshold {score_threshold}")
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    def deduplicate_results(self, results: List[Any]) -> List[Dict[str, Any]]:
        """
        Remove duplicate documents (keep highest scoring chunk per document).
        
        Args:
            results: List of search results
            
        Returns:
            Deduplicated results
        """
        seen_docs = {}
        
        for result in results:
            doc_id = result.payload.get('doc_id')
            score = result.score
            
            if doc_id not in seen_docs or score > seen_docs[doc_id]['score']:
                seen_docs[doc_id] = {
                    'score': score,
                    'result': result
                }
        
        # Sort by score
        deduplicated = sorted(
            seen_docs.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return [item['result'] for item in deduplicated]
    
    def format_results(self, results: List[Any], top_k: int = None) -> List[Dict[str, Any]]:
        """
        Format search results into a clean structure.
        
        Args:
            results: Raw search results
            top_k: Number of top results to return
            
        Returns:
            Formatted results list
        """
        top_k = top_k or RAGConfig.TOP_K_RESULTS
        
        formatted = []
        for i, result in enumerate(results[:top_k]):
            formatted.append({
                'rank': i + 1,
                'score': round(result.score, 4),
                'doc_id': result.payload.get('doc_id'),
                'filename': result.payload.get('filename'),
                'file_path': result.payload.get('file_path'),
                'category': result.payload.get('category'),
                'subcategory': result.payload.get('subcategory'),
                'hierarchy': result.payload.get('hierarchy'),
                'chunk_index': result.payload.get('chunk_index'),
                'chunk_preview': result.payload.get('chunk_text', '')[:200] + '...',
                'full_text_length': result.payload.get('full_text_length')
            })
        
        return formatted
    
    def get_top_templates(
        self, 
        query: str, 
        top_k: int = None,
        category: Optional[str] = None,
        include_scores: bool = True
    ) -> Dict[str, Any]:
        """
        Main method to retrieve top templates for a query.
        
        Args:
            query: User query string
            top_k: Number of templates to return
            category: Filter by specific category
            include_scores: Whether to include similarity scores
            
        Returns:
            Dictionary with query info and results
        """
        logger.info("=" * 60)
        logger.info(f"Retrieving templates for query: '{query}'")
        logger.info("=" * 60)
        
        # Initialize
        self.initialize()
        
        top_k = top_k or RAGConfig.TOP_K_RESULTS
        
        # Process query
        processed_query = self.query_processor.process_query(query)
        query_vector = processed_query['query_vector'].tolist()
        
        # Search
        logger.info(f"Searching for top {top_k} templates...")
        search_results = self.search_similar(
            query_vector=query_vector,
            top_k=top_k,
            category_filter=category
        )
        
        if not search_results:
            logger.warning("No results found!")
            return {
                'success': False,
                'query': query,
                'message': 'No relevant templates found',
                'results': []
            }
        
        # Deduplicate (keep best chunk per document)
        deduplicated_results = self.deduplicate_results(search_results)
        logger.info(f"Deduplicated to {len(deduplicated_results)} unique documents")
        
        # Format results
        formatted_results = self.format_results(deduplicated_results, top_k)
        
        response = {
            'success': True,
            'query': query,
            'preprocessed_query': processed_query['preprocessed_query'],
            'filters': processed_query.get('filters', {}),
            'num_results': len(formatted_results),
            'results': formatted_results
        }
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("Retrieval Results:")
        logger.info("=" * 60)
        for i, result in enumerate(formatted_results, 1):
            logger.info(f"{i}. {result['filename']}")
            logger.info(f"   Score: {result['score']} | Category: {result['category']}")
            logger.info(f"   Path: {result['hierarchy']}")
            logger.info("")
        logger.info("=" * 60)
        
        return response
    
    def retrieve_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve all templates from a specific category.
        
        Args:
            category: Category name
            limit: Maximum number of results
            
        Returns:
            List of templates in the category
        """
        if self.qdrant_client is None:
            self.initialize()
        
        try:
            # Scroll through collection with category filter
            category_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category)
                    )
                ]
            )
            
            results, _ = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                scroll_filter=category_filter,
                limit=limit,
                with_payload=True
            )
            
            # Deduplicate by doc_id
            seen_docs = {}
            for result in results:
                doc_id = result.payload.get('doc_id')
                if doc_id not in seen_docs:
                    seen_docs[doc_id] = result.payload
            
            return list(seen_docs.values())
            
        except Exception as e:
            logger.error(f"Failed to retrieve by category: {str(e)}")
            return []
    
    def get_all_categories(self) -> List[str]:
        """
        Get list of all unique categories in the database.
        
        Returns:
            List of category names
        """
        if self.qdrant_client is None:
            self.initialize()
        
        try:
            # Scroll through all points
            all_points, _ = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust based on your data size
                with_payload=True
            )
            
            # Extract unique categories
            categories = set()
            for point in all_points:
                category = point.payload.get('category')
                if category:
                    categories.add(category)
            
            return sorted(list(categories))
            
        except Exception as e:
            logger.error(f"Failed to get categories: {str(e)}")
            return []


# CLI interface
if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Retrieve templates")
    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--top-k', type=int, default=3, help='Number of results')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    
    args = parser.parse_args()
    
    retriever = TemplateRetriever()
    
    if args.list_categories:
        categories = retriever.get_all_categories()
        print("\nAvailable Categories:")
        print("=" * 40)
        for cat in categories:
            print(f"  - {cat}")
        print("=" * 40)
    else:
        results = retriever.get_top_templates(
            query=args.query,
            top_k=args.top_k,
            category=args.category
        )
        
        print("\n" + json.dumps(results, indent=2))
