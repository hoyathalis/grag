import json
from pathlib import Path
from firebase_admin import credentials, initialize_app, firestore
from typing import Optional
from app.core.logging import logger
from dotenv import load_dotenv
import os

class FirebaseManager:
    def __init__(self):
        self._db: Optional[firestore.Client] = None

    def init_firebase(self) -> None:
        """Initialize Firebase Admin SDK"""

        # Load environment variables from .env file
        load_dotenv()

        # Extract the necessary Firebase credentials from environment variables
        firebase_credentials = {
            "type": os.getenv("FIREBASE_TYPE"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
        }

        # Convert the credentials dictionary to a JSON string
        cred_json = json.dumps(firebase_credentials)

        # Load credentials from the JSON string
        cred = credentials.Certificate(json.loads(cred_json))
        
        try:
            # Initialize the app with credentials
            initialize_app(cred)
        except ValueError:
            # If initialization fails, try initializing without credentials
            initialize_app()

        # Print the project ID we're connected to
        client = firestore.client()
        project_id = client.project
        logger.info(f"Connected to Firebase project: {project_id}")
        # Initialize Firestore client
        self._db = firestore.client()

    def get_db(self) -> firestore.Client:
        """Get the Firestore database instance"""
        if self._db is None:
            self.init_firebase()
        return self._db

firebase_manager = FirebaseManager()
firebase_manager.init_firebase()
logger.info("Firebase initialized")
firebase_db = firebase_manager.get_db()
