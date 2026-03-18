from fastapi import APIRouter, Depends
from app.core.dependencies import get_transcription_service
from app.models.transcription import Transcription, TranscriptionRequest, BatchTranscriptionRequest, BatchTranscriptionResponse
from app.services.transcription_service import TranscriptionService

router = APIRouter(prefix="/transcription", tags=["transcription"])

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/", response_model=Transcription)
def get_phrase_pronunciation(
    request: TranscriptionRequest,
    service: TranscriptionService = Depends(get_transcription_service)
):
    return service.get_phrase_transcription(request.text)

@router.post("/batch", response_model = BatchTranscriptionResponse)
def get_phrase_pronunciations(
    request_texts: BatchTranscriptionRequest,
    service: TranscriptionService = Depends(get_transcription_service)
):
    transcriptions = [service.get_phrase_transcription(text) for text in request_texts.texts]
    return BatchTranscriptionResponse(transcriptions=transcriptions)

@router.get("/{word}", response_model=Transcription)
def get_word_pronunciation(
    word: str,
    service: TranscriptionService = Depends(get_transcription_service)
) -> Transcription:
    return service.get_word_transcription(word)