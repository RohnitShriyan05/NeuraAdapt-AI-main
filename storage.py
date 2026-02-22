import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

from config import settings


class StorageBackend:
    def write_text(self, key: str, content: str) -> str:
        raise NotImplementedError

    def write_json(self, key: str, payload: Dict[str, Any]) -> str:
        return self.write_text(key, json.dumps(payload, indent=2))


class LocalStorage(StorageBackend):
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def write_text(self, key: str, content: str) -> str:
        output_path = os.path.join(self.base_path, key)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return output_path


class S3Storage(StorageBackend):
    def __init__(self, bucket: str, region: str) -> None:
        self.bucket = bucket
        self.client = boto3.client("s3", region_name=region)

    def write_text(self, key: str, content: str) -> str:
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=content.encode("utf-8"))
        except ClientError as exc:
            raise RuntimeError(f"S3 upload failed: {exc}")
        return f"s3://{self.bucket}/{key}"


def get_storage() -> StorageBackend:
    if settings.storage_backend == "s3":
        if not settings.s3_bucket:
            raise ValueError("S3_BUCKET is required when STORAGE_BACKEND=s3")
        return S3Storage(settings.s3_bucket, settings.aws_region)
    return LocalStorage(settings.storage_path)
