"""
Utility functions for RAG system
Common helper functions used across modules
"""

import os
import json
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .config import RAGConfig


def setup_logging():
    """
    Set up logging configuration for the RAG system.
    """
    RAGConfig.create_directories()
    
    logging.basicConfig(
        level=getattr(logging, RAGConfig.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(RAGConfig.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def get_file_hash(file_path: str) -> str:
    """
    Calculate MD5 hash of a file.
    Useful for detecting duplicate files or changes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MD5 hash string
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def save_json(data: Any, file_path: str):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save (must be JSON serializable)
        file_path: Path to save the file
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: str) -> Any:
    """
    Load data from JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Loaded data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove special characters (keep basic punctuation)
    # You can customize this based on your needs
    
    return text.strip()


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def format_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().isoformat()


def create_document_id(file_path: str, chunk_index: int = 0) -> str:
    """
    Create a unique document ID.
    
    Args:
        file_path: Path to the document
        chunk_index: Index of the chunk (for multi-chunk documents)
        
    Returns:
        Unique document ID
    """
    file_hash = get_file_hash(file_path)[:8]
    filename = Path(file_path).stem
    return f"{filename}_{file_hash}_chunk_{chunk_index}"


def extract_metadata_from_path(file_path: str, root_path: str) -> Dict[str, Any]:
    """
    Extract metadata from file path structure.
    
    Args:
        file_path: Full path to the file
        root_path: Root directory path
        
    Returns:
        Dictionary containing extracted metadata
    """
    path_obj = Path(file_path)
    rel_path = path_obj.relative_to(root_path)
    parts = list(rel_path.parts[:-1])  # Exclude filename
    
    metadata = {
        'filename': path_obj.name,
        'file_path': str(file_path),
        'file_size_mb': round(get_file_size_mb(file_path), 2),
        'category': parts[0] if len(parts) > 0 else 'uncategorized',
        'subcategory': parts[1] if len(parts) > 1 else None,
        'hierarchy': ' > '.join(parts) if parts else 'root',
        'depth': len(parts)
    }
    
    return metadata


def chunk_text_fixed(text: str, chunk_size: int, overlap: int, min_size: int) -> List[Dict[str, Any]]:
    """
    Split text into fixed-size chunks with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of overlapping characters
        min_size: Minimum chunk size (discard smaller chunks)
        
    Returns:
        List of chunk dictionaries with text and metadata
    """
    chunks = []
    start = 0
    text_length = len(text)
    chunk_index = 0
    
    while start < text_length:
        end = start + chunk_size
        chunk_text = text[start:end]
        
        # Only add chunk if it meets minimum size
        if len(chunk_text.strip()) >= min_size:
            chunks.append({
                'chunk_index': chunk_index,
                'text': chunk_text.strip(),
                'start_char': start,
                'end_char': end,
                'length': len(chunk_text)
            })
            chunk_index += 1
        
        # Move start position (with overlap)
        start = end - overlap
        
        # Prevent infinite loop
        if start >= text_length or overlap >= chunk_size:
            break
    
    return chunks


def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', length: int = 50):
    """
    Print a progress bar to console.
    
    Args:
        iteration: Current iteration
        total: Total iterations
        prefix: Prefix string
        suffix: Suffix string
        length: Character length of bar
    """
    if total == 0:
        return
    
    percent = 100 * (iteration / float(total))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    
    print(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}', end='')
    
    # Print new line on completion
    if iteration == total:
        print()


def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if valid PDF, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            # Check PDF header
            header = f.read(5)
            return header == b'%PDF-'
    except Exception:
        return False


def get_directory_stats(directory: str) -> Dict[str, Any]:
    """
    Get statistics about a directory.
    
    Args:
        directory: Path to directory
        
    Returns:
        Dictionary with directory statistics
    """
    total_files = 0
    total_size = 0
    file_types = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            
            ext = Path(file).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
    
    return {
        'total_files': total_files,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'file_types': file_types
    }


logger = setup_logging()
