import os


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/neuraadapt")
        self.storage_backend = os.getenv("STORAGE_BACKEND", "local")
        self.storage_path = os.getenv("STORAGE_PATH", "output/sessions")
        self.s3_bucket = os.getenv("S3_BUCKET", "")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.sample_fps = float(os.getenv("SAMPLE_FPS", "15"))
        self.max_frames = int(os.getenv("MAX_FRAMES", "0"))  # 0 means no limit
        self.confusion_threshold = float(os.getenv("CONFUSION_THRESHOLD", "0.7"))
        self.confusion_window_sec = float(os.getenv("CONFUSION_WINDOW_SEC", "3"))
        self.heatmap_bin_sec = float(os.getenv("HEATMAP_BIN_SEC", "1"))


settings = Settings()
