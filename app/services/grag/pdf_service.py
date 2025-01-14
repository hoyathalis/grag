import hashlib
from PyPDF2 import PdfReader
import os
from datetime import datetime
from io import BytesIO

class PdfService:
    def __init__(self):
        self.reader = None

    def generate_pdf_id(self, pdf_input) -> str:
        try:
            # Handle both file path and PDF content
            if isinstance(pdf_input, str):
                self.reader = PdfReader(pdf_input)
                file_size = self._get_file_size(pdf_input)
            else:
                # Assume pdf_input is bytes/BytesIO
                pdf_stream = BytesIO(pdf_input) if isinstance(pdf_input, bytes) else pdf_input
                self.reader = PdfReader(pdf_stream)
                file_size = len(pdf_input) if isinstance(pdf_input, bytes) else pdf_stream.getbuffer().nbytes
            
            # Get metadata and characteristics
            metadata = self.reader.metadata
            page_count = len(self.reader.pages)
            
            # Combine relevant metadata
            # Get all metadata keys
            identifier_parts = [
                str(file_size),
                str(page_count)
            ]
            
            # Add all available metadata values
            if metadata:
                for key, value in metadata.items():
                    identifier_parts.append(f"{key}:{str(value)}")
            
            # Create a unique string from metadata
            content_string = '|'.join(identifier_parts)
            
            # Generate hash
            hash_object = hashlib.sha256(content_string.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def parse_pdf(self, pdf_input) -> str:
        try:
            if isinstance(pdf_input, str):
                self.reader = PdfReader(pdf_input)
            else:
                pdf_stream = BytesIO(pdf_input) if isinstance(pdf_input, bytes) else pdf_input
                self.reader = PdfReader(pdf_stream)
            
            text = ""
            for page in self.reader.pages:
                text += page.extract_text()
            print(text[:100])
            return text
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")