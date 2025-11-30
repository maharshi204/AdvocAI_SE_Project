"""
RAG System for Legal Document Template Retrieval
Provides functionality for ingesting, embedding, and retrieving legal document templates.
"""

__version__ = "1.0.0"
__author__ = "Doc-Gen Team"

from .config import RAGConfig
from .data_ingestion import PDFIngestionPipeline
from .vector_embedding import VectorEmbeddingPipeline
from .query_processor import QueryProcessor
from .retrieval import TemplateRetriever

__all__ = [
    'RAGConfig',
    'PDFIngestionPipeline',
    'VectorEmbeddingPipeline',
    'QueryProcessor',
    'TemplateRetriever',
]
