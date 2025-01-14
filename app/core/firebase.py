import json
from pathlib import Path
from firebase_admin import credentials, initialize_app, firestore
from typing import Optional
from app.core.logging import logger

class FirebaseManager:
    def __init__(self):
        self._db: Optional[firestore.Client] = None

    def init_firebase(self) -> None:
        """Initialize Firebase Admin SDK"""
        # Get the path to firebase.json relative to the project root
        firebase_config_path = Path(__file__).parent.parent.parent / 'firebase.json'
        
        if not firebase_config_path.exists():
            raise FileNotFoundError(f"Firebase configuration file not found at {firebase_config_path}")
        
        # Load credentials from the JSON file
        cred = credentials.Certificate(str(firebase_config_path))
        
        # Initialize the app
        initialize_app(cred)
        
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
