"""Image storage configuration for Cardfolio 2.0."""

import os
from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import UploadFile


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    async def upload_image(self, file: UploadFile, product_id: UUID) -> str:
        """Upload an image and return the URL."""

    @abstractmethod
    async def delete_image(self, image_url: str) -> bool:
        """Delete an image by URL."""

    @abstractmethod
    async def get_image_url(self, image_path: str) -> str:
        """Get the full URL for an image."""


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage backend for development."""

    def __init__(
        self,
        base_path: str = "storage/images",
        base_url: str = "http://localhost:8000/static",
    ):
        self.base_path = base_path
        self.base_url = base_url
        # Create directory if it doesn't exist
        os.makedirs(base_path, exist_ok=True)

    async def upload_image(self, file: UploadFile, product_id: UUID) -> str:
        """Upload an image to local storage."""
        # Generate filename
        file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
        filename = f"{product_id}.{file_extension}"
        file_path = os.path.join(self.base_path, filename)

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Return URL
        return f"{self.base_url}/{filename}"

    async def delete_image(self, image_url: str) -> bool:
        """Delete an image from local storage."""
        try:
            filename = image_url.split("/")[-1]
            file_path = os.path.join(self.base_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    async def get_image_url(self, image_path: str) -> str:
        """Get the full URL for an image."""
        return f"{self.base_url}/{image_path}"


class SupabaseStorageBackend(StorageBackend):
    """Supabase storage backend for production."""

    def __init__(
        self, supabase_url: str, supabase_key: str, bucket_name: str = "card-images"
    ):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.bucket_name = bucket_name
        # TODO: Initialize Supabase client when we add supabase-py dependency

    async def upload_image(self, file: UploadFile, product_id: UUID) -> str:
        """Upload an image to Supabase Storage."""
        # TODO: Implement Supabase upload
        # For now, return a placeholder URL
        file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
        filename = f"{product_id}.{file_extension}"
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{filename}"

    async def delete_image(self, image_url: str) -> bool:
        """Delete an image from Supabase Storage."""
        # TODO: Implement Supabase delete
        return True

    async def get_image_url(self, image_path: str) -> str:
        """Get the full URL for an image."""
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{image_path}"


class MinIOStorageBackend(StorageBackend):
    """MinIO storage backend for development with Docker Compose."""

    def __init__(
        self, endpoint: str = "localhost:9000", bucket_name: str = "card-images"
    ):
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        # TODO: Initialize MinIO client when we add minio dependency

    async def upload_image(self, file: UploadFile, product_id: UUID) -> str:
        """Upload an image to MinIO."""
        # TODO: Implement MinIO upload
        file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
        filename = f"{product_id}.{file_extension}"
        return f"http://{self.endpoint}/{self.bucket_name}/{filename}"

    async def delete_image(self, image_url: str) -> bool:
        """Delete an image from MinIO."""
        # TODO: Implement MinIO delete
        return True

    async def get_image_url(self, image_path: str) -> str:
        """Get the full URL for an image."""
        return f"http://{self.endpoint}/{self.bucket_name}/{image_path}"


def get_storage_backend() -> StorageBackend:
    """Get the configured storage backend."""
    storage_type = os.getenv("STORAGE_TYPE", "local")

    if storage_type == "supabase":
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set for Supabase storage"
            )
        return SupabaseStorageBackend(supabase_url, supabase_key)

    if storage_type == "minio":
        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        return MinIOStorageBackend(endpoint)

    # default to local
    return LocalStorageBackend()


# Global storage instance
storage = get_storage_backend()
