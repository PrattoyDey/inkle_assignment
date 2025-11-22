import os


class Config:
    # SQLite DB (file in project root)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///inkle.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Change this in production (set env var in Render)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")

    # Optional: CORS
    CORS_HEADERS = "Content-Type"