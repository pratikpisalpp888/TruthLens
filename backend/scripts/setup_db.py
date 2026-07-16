import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add the parent directory to sys.path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

async def setup_database():
    print("Setting up PostgreSQL database...")
    
    # We need to connect to the default 'postgres' database to create a new one
    # We'll parse the DATABASE_URL to get the credentials, but connect to 'postgres'
    url = settings.DATABASE_URL
    if not url.startswith("postgresql+asyncpg"):
        print(f"Error: DATABASE_URL must start with postgresql+asyncpg. Currently: {url}")
        return
        
    # Extract the base URL without the database name
    base_url = url.rsplit("/", 1)[0]
    db_name = url.rsplit("/", 1)[1]
    
    postgres_url = f"{base_url}/postgres"
    
    try:
        # Create engine connecting to default postgres database
        engine = create_async_engine(postgres_url, isolation_level="AUTOCOMMIT")
        
        async with engine.connect() as conn:
            # Check if database exists
            result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            exists = result.scalar()
            
            if not exists:
                print(f"Creating database '{db_name}'...")
                await conn.execute(text(f"CREATE DATABASE {db_name}"))
                print("Database created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
                
        await engine.dispose()
        
        print("\nDatabase setup complete. You can now run migrations:")
        print("alembic upgrade head")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        print("\nPlease ensure PostgreSQL is running and the credentials in .env are correct.")

if __name__ == "__main__":
    asyncio.run(setup_database())
