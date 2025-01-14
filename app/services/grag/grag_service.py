from app.core.graphrag_config import generate_grag_config
from app.core.firebase import firebase_db
from firebase_admin import firestore
from app.services.grag.pdf_service import PdfService
import graphrag.api as api
from graphrag.index.typing import PipelineRunResult
from graphrag.config.create_graphrag_config import create_graphrag_config
import os
from pathlib import Path
import pandas as pd
import uuid
import asyncio
from fastapi import UploadFile
import logging

class GragService:
    def __init__(self):
        self.pdf_service = PdfService()

    async def create_grag_request(self, file: UploadFile):
        if not file.filename.lower().endswith('.pdf'):
            raise ValueError("Uploaded file must be a PDF")

        request_id = str(uuid.uuid4())
        file_content = await file.read()
        pdf_id = self.pdf_service.generate_pdf_id(file_content)

        firebase_db.collection('grag_requests').document(request_id).set({
            'status': 'in_progress',
            'filename': file.filename,
            'pdf_id': pdf_id,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        })

        base_dir = Path(__file__).resolve().parent.parent.parent.parent / 'data' / 'uploads'
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, f"{pdf_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            f.write(file_content)

        asyncio.create_task(self._process_grag_request(request_id, file_path, pdf_id))
        return {'request_id': request_id, 'pdf_id': pdf_id}

    async def _process_grag_request(self, request_id: str, file_path: str, pdf_id: str):
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Starting to process grag request {request_id} for PDF {pdf_id}")
            pdf_text = self.pdf_service.parse_pdf(file_path)
            logger.info(f"Successfully parsed PDF for request {request_id}")
            
            # Delete the file after parsing
            os.remove(file_path)
            logger.info(f"Deleted temporary PDF file: {file_path}")

            result = await self.get_grag_data(pdf_id=pdf_id, story=pdf_text)
            logger.info(f"Successfully generated grag data for request {request_id}")
            
            firebase_db.collection('grag_requests').document(request_id).update({
                'status': 'success',
                'data': result,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            logger.info(f"Successfully updated Firebase for request {request_id}")
        except Exception as e:
            logger.error(f"Error processing request {request_id}: {str(e)}", exc_info=True)
            firebase_db.collection('grag_requests').document(request_id).update({
                'status': 'failed',
                'error': str(e),
                'updated_at': firestore.SERVER_TIMESTAMP
            })

    async def get_grag_request(self, request_id: str):
        doc = firebase_db.collection('grag_requests').document(request_id).get()
        if not doc.exists:
            raise ValueError(f"No grag request found with id: {request_id}")
        return doc.to_dict()

    async def get_grag_data(self, pdf_id: str, story: str):
        user_id = "hoyath"

        current_config = generate_grag_config(user_id=user_id, pdf_id=pdf_id)
        
        # Write story before building index
        os.makedirs(current_config['pdf_input_dir'], exist_ok=True)
        with open(os.path.join(current_config['pdf_input_dir'], "paper.txt"), "w", encoding='utf-8') as f:
            f.write(story)

        graphrag_config = create_graphrag_config(values=current_config, root_dir="./")
        
        await api.build_index(config=graphrag_config)
        
        # Read parquet files after index is built
        nodes_path = os.path.join(current_config['pdf_output_dir'], 'create_final_nodes.parquet')
        rels_path = os.path.join(current_config['pdf_output_dir'], 'create_final_relationships.parquet')
        
        if not (os.path.exists(nodes_path) and os.path.exists(rels_path)):
            raise FileNotFoundError("Parquet files were not created during index building")
                   
        nodes_df = pd.read_parquet(nodes_path)
        rels_df = pd.read_parquet(rels_path)

        nodes_list = []
        seen_ids = set()
        for _, row in nodes_df.iterrows():
            if row['id'] not in seen_ids:
                nodes_list.append({
                    'id': row['id'],
                    'human_readable_id': row['human_readable_id'],
                    'title': row['title'],
                    'community': row['community'],
                    'level': row['level'],
                    'degree': row['degree'],
                    'x': row['x'],
                    'y': row['y']
                })
                seen_ids.add(row['id'])

        rels_list = [{ 
            'human_readable_id': str(row['human_readable_id']),
            'source': str(row['source']),
            'target': str(row['target']), 
            'weight': float(row['weight']),
            'combined_degree': int(row['combined_degree']), 
            'text_unit_ids': row['text_unit_ids'].tolist() if isinstance(row['text_unit_ids'], (pd.Series, list)) else str(row['text_unit_ids'])
        } for _, row in rels_df.iterrows()]

        return {'nodes': nodes_list, 'relationships': rels_list}
