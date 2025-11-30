"""
Configuration file for RAG System
Centralized configuration for all RAG components
"""

import os
from pathlib import Path

class RAGConfig:
    """
    Central configuration for the RAG system.
    Modify these settings to customize behavior.
    """
    
    # ============================================
    # PATH CONFIGURATION
    # ============================================
    
    # Root directory for the project
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # PDF Templates Location - YOUR DATA PATH
    PDF_ROOT_PATH = r"C:\Users\mahar\OneDrive\Desktop\Kaggle\CUAD_v1\CUAD_v1\full_contract_pdf"
    
    # Processed data storage
    PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
    METADATA_DIR = BASE_DIR / "data" / "metadata"
    
    # Qdrant storage location (for embedded mode)
    QDRANT_STORAGE_PATH = BASE_DIR / "qdrant_data"
    
    # ============================================
    # QDRANT CONFIGURATION
    # ============================================
    
    # Mode: "embedded" (local), "server" (Docker), or "cloud" (Qdrant Cloud)
    QDRANT_MODE = "embedded"  # Start with embedded, switch later if needed
    
    # Server mode configuration (for Docker)
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    
    # Cloud mode configuration (for production)
    QDRANT_URL = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
    
    # Collection name in Qdrant
    COLLECTION_NAME = "legal_document_templates"
    
    # ============================================
    # EMBEDDING MODEL CONFIGURATION
    # ============================================
    
    # Embedding model name (HuggingFace)
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Vector dimension (all-MiniLM-L6-v2 produces 384-dim vectors)
    VECTOR_DIM = 384
    
    # Model cache directory
    MODEL_CACHE_DIR = Path.home() / ".cache" / "torch" / "sentence_transformers"
    
    # Batch size for embedding generation
    EMBEDDING_BATCH_SIZE = 32
    
    # Device for computation ('cuda' for GPU, 'cpu' for CPU)
    DEVICE = "cpu"  # Change to "cuda" if you have GPU
    
    # ============================================
    # PDF PROCESSING CONFIGURATION
    # ============================================
    
    # Enable recursive scanning of subdirectories
    RECURSIVE_SCAN = True
    
    # File patterns to include
    INCLUDE_PATTERNS = ["*.pdf", "*.PDF"]
    
    # Folders to exclude during scanning
    EXCLUDE_FOLDERS = ["__pycache__", "temp", ".git", "node_modules"]
    
    # Extract category from folder structure
    EXTRACT_CATEGORY_FROM_PATH = True
    
    # Maximum folder depth (-1 for unlimited)
    MAX_FOLDER_DEPTH = -1
    
    # ============================================
    # TEXT CHUNKING CONFIGURATION
    # ============================================
    
    # Chunk size in characters
    CHUNK_SIZE = 1000
    
    # Overlap between chunks (to preserve context)
    CHUNK_OVERLAP = 200
    
    # Minimum chunk size (discard smaller chunks)
    MIN_CHUNK_SIZE = 100
    
    # Chunking strategy: "fixed" or "semantic"
    CHUNKING_STRATEGY = "fixed"  # Start with fixed, can implement semantic later
    
    # ============================================
    # RETRIEVAL CONFIGURATION
    # ============================================
    
    # Number of top results to return
    TOP_K_RESULTS = 3
    
    # Minimum similarity score threshold (0.0 to 1.0)
    MIN_SIMILARITY_SCORE = 0.5
    
    # Enable re-ranking of results
    ENABLE_RERANKING = False
    
    # ============================================
    # LOGGING CONFIGURATION
    # ============================================
    
    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = "INFO"
    
    # Log file location
    LOG_FILE = BASE_DIR / "rag_system.log"
    
    # ============================================
    # PERFORMANCE CONFIGURATION
    # ============================================
    
    # Enable progress bars during processing
    SHOW_PROGRESS = True
    
    # Number of workers for parallel processing
    NUM_WORKERS = 4
    
    # Cache embeddings to avoid recomputation
    CACHE_EMBEDDINGS = True
    
    @classmethod
    def get_qdrant_client(cls):
        """
        Factory method to create appropriate Qdrant client based on mode.
        """
        from qdrant_client import QdrantClient
        
        if cls.QDRANT_MODE == "embedded":
            # Local embedded mode (no Docker needed)
            return QdrantClient(path=str(cls.QDRANT_STORAGE_PATH))
        
        elif cls.QDRANT_MODE == "server":
            # Docker/Server mode
            return QdrantClient(host=cls.QDRANT_HOST, port=cls.QDRANT_PORT)
        
        elif cls.QDRANT_MODE == "cloud":
            # Qdrant Cloud mode
            return QdrantClient(url=cls.QDRANT_URL, api_key=cls.QDRANT_API_KEY)
        
        else:
            raise ValueError(f"Invalid QDRANT_MODE: {cls.QDRANT_MODE}")
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.METADATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.QDRANT_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_paths(cls):
        """Validate that required paths exist."""
        if not Path(cls.PDF_ROOT_PATH).exists():
            raise FileNotFoundError(
                f"PDF root path does not exist: {cls.PDF_ROOT_PATH}\n"
                "Please update PDF_ROOT_PATH in config.py"
            )
