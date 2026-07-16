"""
TruthLens — Startup Initialization Script.
"""

import asyncio
import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings


async def initialize_system():
    print("=" * 60)
    print(" TruthLens — Startup Initialization")
    print(f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ── 1. Database ──────────────────────────────────────────────
    print("\n[1/7] Initializing database...")
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy import text
        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("      ✅ CockroachDB connected")
    except Exception as e:
        print(f"      ❌ CockroachDB: {e}")

    # ── 2. Run Alembic Migrations ────────────────────────────────
    print("\n[2/7] Running Alembic migrations...")
    try:
        import subprocess
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        if result.returncode == 0:
            print("      ✅ Migrations applied")
        else:
            print(f"      ⚠️  Alembic: {result.stderr[:200]}")
    except Exception as e:
        print(f"      ⚠️  Migrations skipped: {e}")

    # ── 3. Seed Admin User ───────────────────────────────────────
    print("\n[3/7] Seeding admin user...")
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy import select
        from app.db.models.user import User
        from app.core.security import hash_password

        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == "admin@canara.bank"))
            existing = result.scalars().first()
            if not existing:
                import uuid
                admin = User(
                    id=uuid.uuid4(),
                    email="admin@canara.bank",
                    password_hash=hash_password("Admin@TruthLens123"),
                    full_name="System Administrator",
                    role="admin",
                    is_active=True
                )
                session.add(admin)
                await session.commit()
                print("      ✅ Admin user created: admin@canara.bank / Admin@TruthLens123")
            else:
                print("      ✅ Admin user already exists")
        await engine.dispose()
    except Exception as e:
        print(f"      ⚠️  Admin seed: {e}")

    # ── 4. MinIO Bucket ──────────────────────────────────────────
    print("\n[4/7] Verifying MinIO bucket...")
    try:
        from minio import Minio
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        if not client.bucket_exists(settings.MINIO_BUCKET):
            client.make_bucket(settings.MINIO_BUCKET)
            print(f"      ✅ Bucket '{settings.MINIO_BUCKET}' created")
        else:
            print(f"      ✅ Bucket '{settings.MINIO_BUCKET}' exists")
    except Exception as e:
        print(f"      ❌ MinIO: {e}")

    # ── 5. Qdrant Collections ────────────────────────────────────
    print("\n[5/7] Verifying Qdrant collections...")
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams
        qdrant = QdrantClient(path=settings.QDRANT_PATH)
        for col_name in ["knowledge_base", "fraud_patterns"]:
            try:
                qdrant.get_collection(col_name)
                print(f"      ✅ Collection '{col_name}' exists")
            except Exception:
                qdrant.create_collection(
                    collection_name=col_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                print(f"      ✅ Collection '{col_name}' created")
    except Exception as e:
        print(f"      ❌ Qdrant: {e}")

    # ── 6. Knowledge Base ────────────────────────────────────────
    print("\n[6/7] Loading knowledge base...")
    try:
        from app.rag.knowledge_loader import KnowledgeBaseLoader
        loader = KnowledgeBaseLoader()
        is_loaded = await loader.is_loaded()
        if not is_loaded:
            print("      📚 Indexing knowledge base documents...")
            await loader.load_and_index()
            print("      ✅ Knowledge base indexed")
        else:
            count = loader.qdrant.count("knowledge_base").count
            print(f"      ✅ Knowledge base already loaded ({count} chunks)")
    except Exception as e:
        print(f"      ⚠️  Knowledge base: {e}")

    # ── 7. Ollama Model ──────────────────────────────────────────
    print("\n[7/7] Verifying Ollama model...")
    try:
        import httpx
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            models = resp.json().get("models", [])
            names = [m.get("name") for m in models]
            model_ok = any(settings.OLLAMA_MODEL in n for n in names)
            if model_ok:
                print(f"      ✅ Model '{settings.OLLAMA_MODEL}' loaded")
            if not model_ok:
                print(f"      ⚠️  Model '{settings.OLLAMA_MODEL}' not found. Pull with: docker exec ollama ollama pull {settings.OLLAMA_MODEL}")
            
            print(f"      ✓ Ollama API reachable ({len(models)} models found)")
    except Exception as e:
        print(f"      ❌ Ollama: {e}")

    print("\n" + "=" * 60)
    print(" ✅ TruthLens initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(initialize_system())
