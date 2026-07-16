import sys
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Add the parent directory to sys.path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

def setup_qdrant():
    print(f"Setting up Qdrant (Mode: {settings.QDRANT_MODE})...")
    
    try:
        # Connect to Qdrant based on settings
        if settings.QDRANT_MODE.lower() == "memory":
            print("Using in-memory Qdrant (Data will be lost on restart)")
            client = QdrantClient(":memory:")
        elif settings.QDRANT_MODE.lower() == "persistent":
            print(f"Using persistent Qdrant at {settings.QDRANT_PATH}")
            # Ensure path exists
            os.makedirs(settings.QDRANT_PATH, exist_ok=True)
            client = QdrantClient(path=settings.QDRANT_PATH)
        else:
            # Assume connecting to a server (like the binary or docker)
            print(f"Connecting to Qdrant server at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
            
        collections_res = client.get_collections().collections
        existing = [c.name for c in collections_res]
        
        # Create knowledge_base collection
        print("Checking 'knowledge_base' collection...")
        if "knowledge_base" not in existing:
            print("Creating 'knowledge_base' collection...")
            client.create_collection(
                collection_name="knowledge_base",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print("Collection 'knowledge_base' created.")
        else:
            print("Collection 'knowledge_base' already exists.")
            
        # Create fraud_patterns collection
        print("Checking 'fraud_patterns' collection...")
        if "fraud_patterns" not in existing:
            print("Creating 'fraud_patterns' collection...")
            client.create_collection(
                collection_name="fraud_patterns",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print("Collection 'fraud_patterns' created.")
        else:
            print("Collection 'fraud_patterns' already exists.")
            
        print("\nQdrant setup complete!")
        
    except Exception as e:
        print(f"Error setting up Qdrant: {e}")
        if "connection refused" in str(e).lower():
            print("\nPlease ensure Qdrant is running if you are not using memory/persistent mode.")

if __name__ == "__main__":
    setup_qdrant()
