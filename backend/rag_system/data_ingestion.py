"""
File 1: Data Ingestion Pipeline
Handles PDF extraction, text processing, and metadata extraction
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import PyPDF2
import pdfplumber

from .config import RAGConfig
from .utils import (
    logger, 
    extract_metadata_from_path, 
    chunk_text_fixed,
    validate_pdf_file,
    get_file_hash,
    save_json,
    format_timestamp
)


class PDFIngestionPipeline:
    """
    Pipeline for ingesting PDF documents and extracting text content.
    Handles recursive directory scanning, PDF text extraction, and chunking.
    """
    
    def __init__(self, root_path: Optional[str] = None):
        """
        Initialize the PDF ingestion pipeline.
        
        Args:
            root_path: Root directory containing PDF files (defaults to config)
        """
        self.root_path = root_path or RAGConfig.PDF_ROOT_PATH
        self.processed_docs = []
        self.failed_docs = []
        
        logger.info(f"Initialized PDFIngestionPipeline with root: {self.root_path}")
    
    def scan_directory(self) -> List[str]:
        """
        Recursively scan directory for PDF files.
        
        Returns:
            List of PDF file paths
        """
        logger.info(f"Scanning directory: {self.root_path}")
        pdf_files = []
        
        root_path = Path(self.root_path)
        
        if RAGConfig.RECURSIVE_SCAN:
            # Recursively find all PDFs
            for pattern in RAGConfig.INCLUDE_PATTERNS:
                found_files = list(root_path.rglob(pattern))
                pdf_files.extend(found_files)
        else:
            # Only top-level directory
            for pattern in RAGConfig.INCLUDE_PATTERNS:
                found_files = list(root_path.glob(pattern))
                pdf_files.extend(found_files)
        
        # Filter out excluded folders
        pdf_files = [
            f for f in pdf_files 
            if not any(excluded in f.parts for excluded in RAGConfig.EXCLUDE_FOLDERS)
        ]
        
        # Convert to strings and remove duplicates
        pdf_files = list(set(str(f) for f in pdf_files))
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        return pdf_files
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file using multiple methods.
        Tries pdfplumber first, falls back to PyPDF2.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text or None if extraction fails
        """
        text_content = ""
        
        # Method 1: Try pdfplumber (better for complex PDFs)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n\n"
            
            if text_content.strip():
                logger.debug(f"Extracted text using pdfplumber: {pdf_path}")
                return text_content.strip()
        except Exception as e:
            logger.warning(f"pdfplumber failed for {pdf_path}: {str(e)}")
        
        # Method 2: Fallback to PyPDF2
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n\n"
            
            if text_content.strip():
                logger.debug(f"Extracted text using PyPDF2: {pdf_path}")
                return text_content.strip()
        except Exception as e:
            logger.error(f"PyPDF2 failed for {pdf_path}: {str(e)}")
        
        return None
    
    def process_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a single PDF file: extract text, metadata, and create chunks.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary containing processed document data
        """
        # Validate PDF
        if not validate_pdf_file(pdf_path):
            logger.warning(f"Invalid PDF file: {pdf_path}")
            return None
        
        # Extract text
        text_content = self.extract_text_from_pdf(pdf_path)
        if not text_content:
            logger.warning(f"No text extracted from: {pdf_path}")
            return None
        
        # Extract metadata from path
        metadata = extract_metadata_from_path(pdf_path, self.root_path)
        
        # Create chunks
        chunks = chunk_text_fixed(
            text_content,
            RAGConfig.CHUNK_SIZE,
            RAGConfig.CHUNK_OVERLAP,
            RAGConfig.MIN_CHUNK_SIZE
        )
        
        # Create document object
        doc_data = {
            'doc_id': get_file_hash(pdf_path)[:16],
            'metadata': metadata,
            'text_content': text_content,
            'chunks': chunks,
            'num_chunks': len(chunks),
            'total_length': len(text_content),
            'processed_at': format_timestamp()
        }
        
        logger.debug(f"Processed: {metadata['filename']} - {len(chunks)} chunks")
        return doc_data
    
    def get_category_structure(self, pdf_files: List[str]) -> Dict[str, Any]:
        """
        Analyze the folder structure to extract categories.
        
        Args:
            pdf_files: List of PDF file paths
            
        Returns:
            Dictionary with category structure
        """
        categories = {}
        
        for pdf_path in pdf_files:
            metadata = extract_metadata_from_path(pdf_path, self.root_path)
            category = metadata['category']
            subcategory = metadata.get('subcategory')
            
            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'subcategories': {}
                }
            
            categories[category]['count'] += 1
            
            if subcategory:
                if subcategory not in categories[category]['subcategories']:
                    categories[category]['subcategories'][subcategory] = 0
                categories[category]['subcategories'][subcategory] += 1
        
        return categories
    
    def ingest_all(self, save_output: bool = True) -> Dict[str, Any]:
        """
        Main method to ingest all PDF files.
        
        Args:
            save_output: Whether to save processed data to disk
            
        Returns:
            Dictionary with ingestion statistics
        """
        logger.info("=" * 60)
        logger.info("Starting PDF Ingestion Pipeline")
        logger.info("=" * 60)
        
        # Scan for PDFs
        pdf_files = self.scan_directory()
        
        if not pdf_files:
            logger.error("No PDF files found!")
            return {'success': False, 'message': 'No PDF files found'}
        
        # Analyze category structure
        category_structure = self.get_category_structure(pdf_files)
        logger.info(f"\nFound {len(category_structure)} categories:")
        for cat, data in category_structure.items():
            logger.info(f"  ├── {cat}: {data['count']} files")
            for subcat, count in data['subcategories'].items():
                logger.info(f"  │   └── {subcat}: {count} files")
        
        # Process all PDFs
        logger.info(f"\nProcessing {len(pdf_files)} PDF files...")
        
        self.processed_docs = []
        self.failed_docs = []
        
        # Use tqdm for progress bar if enabled
        iterator = tqdm(pdf_files, desc="Processing PDFs") if RAGConfig.SHOW_PROGRESS else pdf_files
        
        for pdf_path in iterator:
            try:
                doc_data = self.process_pdf(pdf_path)
                if doc_data:
                    self.processed_docs.append(doc_data)
                else:
                    self.failed_docs.append(pdf_path)
            except Exception as e:
                logger.error(f"Error processing {pdf_path}: {str(e)}")
                self.failed_docs.append(pdf_path)
        
        # Calculate statistics
        total_chunks = sum(doc['num_chunks'] for doc in self.processed_docs)
        
        stats = {
            'success': True,
            'total_files': len(pdf_files),
            'processed': len(self.processed_docs),
            'failed': len(self.failed_docs),
            'total_chunks': total_chunks,
            'categories': category_structure,
            'processed_at': format_timestamp()
        }
        
        # Save output if requested
        if save_output:
            self._save_processed_data(stats)
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("Ingestion Complete!")
        logger.info("=" * 60)
        logger.info(f"✅ Successfully processed: {stats['processed']} files")
        logger.info(f"❌ Failed to process: {stats['failed']} files")
        logger.info(f"📄 Total text chunks created: {stats['total_chunks']}")
        logger.info(f"💾 Data saved to: {RAGConfig.PROCESSED_DATA_DIR}")
        logger.info("=" * 60)
        
        return stats
    
    def _save_processed_data(self, stats: Dict[str, Any]):
        """
        Save processed documents and metadata to disk.
        
        Args:
            stats: Statistics dictionary
        """
        RAGConfig.create_directories()
        
        # Save individual documents
        for doc in self.processed_docs:
            filename = f"{doc['doc_id']}.json"
            filepath = RAGConfig.PROCESSED_DATA_DIR / filename
            save_json(doc, str(filepath))
        
        # Save metadata
        metadata_file = RAGConfig.METADATA_DIR / "ingestion_stats.json"
        save_json(stats, str(metadata_file))
        
        # Save failed files list
        if self.failed_docs:
            failed_file = RAGConfig.METADATA_DIR / "failed_files.json"
            save_json(self.failed_docs, str(failed_file))
        
        logger.info(f"Saved {len(self.processed_docs)} processed documents")
    
    def get_processed_documents(self) -> List[Dict[str, Any]]:
        """
        Get list of processed documents.
        
        Returns:
            List of processed document dictionaries
        """
        return self.processed_docs


# CLI interface for direct execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest PDF documents")
    parser.add_argument('--path', type=str, help='Path to PDF directory', default=None)
    args = parser.parse_args()
    
    pipeline = PDFIngestionPipeline(root_path=args.path)
    stats = pipeline.ingest_all()
    
    print(json.dumps(stats, indent=2))
