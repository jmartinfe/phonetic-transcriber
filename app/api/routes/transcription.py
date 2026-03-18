from fastapi import APIRouter, Depends
from app.core.dependencies import get_transcription_service
from app.models.transcription import Transcription
from app.services.transcription_service import TranscriptionService

router = APIRouter(prefix="/transcription", tags=["transcription"])

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/transcription/{text}")
def get_phrase_pronunciation(
    text: str,
    service: TranscriptionService = Depends(get_transcription_service)
) -> Transcription:
    return service.get_phrase_transcription(text)