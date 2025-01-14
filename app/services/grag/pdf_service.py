import hashlib
from PyPDF2 import PdfReader
import os
from datetime import datetime
from io import BytesIO

class PdfService:
    def __init__(self):
        pass  

    def generate_pdf_id(self, pdf_input) -> str:
        try:
            # Create reader locally for this request
            if isinstance(pdf_input, str):
                reader = PdfReader(pdf_input)
                file_size = self._get_file_size(pdf_input)
            else:
                pdf_stream = BytesIO(pdf_input) if isinstance(pdf_input, bytes) else pdf_input
                reader = PdfReader(pdf_stream)
                file_size = len(pdf_input) if isinstance(pdf_input, bytes) else pdf_stream.getbuffer().nbytes
            
            # Use local reader instance
            metadata = reader.metadata
            page_count = len(reader.pages)
            
            identifier_parts = [
                str(file_size),
                str(page_count)
            ]
            
            if metadata:
                for key, value in metadata.items():
                    identifier_parts.append(f"{key}:{str(value)}")
            
            content_string = '|'.join(identifier_parts)
            hash_object = hashlib.sha256(content_string.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def parse_pdf(self, pdf_input) -> str:
        try:
            # Create reader locally for this request
            if isinstance(pdf_input, str):
                reader = PdfReader(pdf_input)
            else:
                pdf_stream = BytesIO(pdf_input) if isinstance(pdf_input, bytes) else pdf_input
                reader = PdfReader(pdf_stream)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")