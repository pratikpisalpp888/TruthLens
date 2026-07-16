"""
TruthLens — MinIO Storage Service.
"""

import os
import asyncio
from typing import Optional
from io import BytesIO
from datetime import timedelta
from minio.error import S3Error
import uuid

from app.core.config import settings
from app.core.exceptions import StorageException, FileNotFoundInStorageError

class StorageService:
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE.lower()
        if self.storage_type == "local":
            self.base_path = os.path.abspath(settings.STORAGE_PATH)
            os.makedirs(self.base_path, exist_ok=True)
        else:
            from minio import Minio
            # Safe import since MinIO is only needed if not local
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False,
            )
            self.bucket = settings.MINIO_BUCKET

    async def ensure_bucket(self):
        if self.storage_type == "local":
            return
        
        loop = asyncio.get_event_loop()
        def _create_bucket():
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        await loop.run_in_executor(None, _create_bucket)

    async def upload(self, path: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        if self.storage_type == "local":
            full_path = os.path.join(self.base_path, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            try:
                import aiofiles
                async with aiofiles.open(full_path, 'wb') as f:
                    await f.write(data)
                return path
            except Exception as e:
                raise StorageException(f"Failed to upload object locally: {e}")

        loop = asyncio.get_event_loop()
        def _upload():
            self.client.put_object(
                self.bucket,
                path,
                BytesIO(data),
                length=len(data),
                content_type=content_type
            )
        try:
            await loop.run_in_executor(None, _upload)
            return path
        except Exception as e:
            raise StorageException(f"Failed to upload object to MinIO: {e}")

    async def download(self, path: str) -> bytes:
        if self.storage_type == "local":
            full_path = os.path.join(self.base_path, path)
            if not os.path.exists(full_path):
                raise FileNotFoundInStorageError()
            try:
                import aiofiles
                async with aiofiles.open(full_path, 'rb') as f:
                    return await f.read()
            except Exception as e:
                raise StorageException(f"Failed to download object locally: {e}")

        loop = asyncio.get_event_loop()
        def _download():
            try:
                response = self.client.get_object(self.bucket, path)
                data = response.read()
                response.close()
                response.release_conn()
                return data
            except S3Error as e:
                if e.code == "NoSuchKey":
                    raise FileNotFoundInStorageError()
                raise e
        try:
            return await loop.run_in_executor(None, _download)
        except FileNotFoundInStorageError:
            raise
        except Exception as e:
            raise StorageException(f"Failed to download object from MinIO: {e}")

    async def delete(self, path: str) -> bool:
        if self.storage_type == "local":
            full_path = os.path.join(self.base_path, path)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception as e:
                    raise StorageException(f"Failed to delete object locally: {e}")
            return True

        loop = asyncio.get_event_loop()
        def _delete():
            self.client.remove_object(self.bucket, path)
        try:
            await loop.run_in_executor(None, _delete)
            return True
        except Exception as e:
            raise StorageException(f"Failed to delete object from MinIO: {e}")

    async def get_presigned_url(self, path: str, expires_minutes: int = 60) -> str:
        if self.storage_type == "local":
            # In a real app we might route to a download endpoint
            # For now, we will return a mock URL or an API endpoint route
            return f"http://localhost:8000/api/v1/documents/download/{path}"

        loop = asyncio.get_event_loop()
        def _get_url():
            return self.client.presigned_get_object(self.bucket, path, expires=timedelta(minutes=expires_minutes))
        try:
            return await loop.run_in_executor(None, _get_url)
        except Exception as e:
            raise StorageException(f"Failed to generate presigned URL: {e}")
