from fastapi import FastAPI
from app.core.logging_config import setup_logging
from app.api.routes.transcription import router as pronunciation_router


def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(title="Phonetic Transcriber API")

    app.include_router(pronunciation_router)

    return app


app = create_app()