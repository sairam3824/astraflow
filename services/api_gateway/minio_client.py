from minio import Minio
from datetime import timedelta
from libs.utils.config import config

class MinIOClient:
    def __init__(self):
        self.client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False
        )
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        if not self.client.bucket_exists(config.MINIO_BUCKET):
            self.client.make_bucket(config.MINIO_BUCKET)
    
    def generate_presigned_url(self, object_name: str) -> str:
        return self.client.presigned_put_object(
            config.MINIO_BUCKET,
            object_name,
            expires=timedelta(hours=1)
        )
    
    def get_object_url(self, object_name: str) -> str:
        return self.client.presigned_get_object(
            config.MINIO_BUCKET,
            object_name,
            expires=timedelta(hours=1)
        )

minio_client = MinIOClient()
