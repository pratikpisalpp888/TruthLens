"""
TruthLens — Seed Knowledge Base Script.
"""

import asyncio
import sys
import os

# Ensure imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.knowledge_loader import KnowledgeBaseLoader

async def main():
    print("Loading and indexing knowledge base into Qdrant...")
    loader = KnowledgeBaseLoader()
    await loader.load_and_index()
    count_ok = await loader.is_loaded()
    if count_ok:
        print("Knowledge base loaded successfully.")
    else:
        print("WARNING: Knowledge base may be empty. Check data/knowledge_base directory.")

if __name__ == "__main__":
    asyncio.run(main())
