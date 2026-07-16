"""
TruthLens — Admin Seeding Script.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def seed_admin():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Check if admin exists
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.email == "admin@truthlens.ai"))
        admin = result.scalars().first()
        
        if not admin:
            print("Creating default admin user...")
            admin = User(
                email="admin@truthlens.ai",
                password_hash=get_password_hash("admin123"),
                full_name="System Administrator",
                role="admin"
            )
            session.add(admin)
        else:
            print("Admin user already exists.")
            
        result = await session.execute(select(User).where(User.email == "officer@truthlens.ai"))
        officer = result.scalars().first()
        
        if not officer:
            print("Creating sample officer user...")
            officer = User(
                email="officer@truthlens.ai",
                password_hash=get_password_hash("officer123"),
                full_name="Sample Loan Officer",
                role="officer"
            )
            session.add(officer)
        else:
            print("Officer user already exists.")

        await session.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_admin())
