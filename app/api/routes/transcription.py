from fastapi import APIRouter, Depends
from app.core.dependencies import get_transcription_service
from app.models.transcription import Transcription, TranscriptionRequest, BatchTranscriptionRequest, BatchTranscriptionResponse
from app.models.formatter import FormattedTextTranscription
from app.services.transcription_service import TranscriptionService
from app.formatter.transcription_formatter import transcription_to_formatted_text_transcription

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

@router.post("/formatted/", response_model=FormattedTextTranscription)
def get_formatted_text_pronunciation(
    request: TranscriptionRequest,
    transcription_service: TranscriptionService = Depends(get_transcription_service)
) -> FormattedTextTranscription:
    raw_transcription = transcription_service.get_phrase_transcription(request.text)
    return transcription_to_formatted_text_transcription(raw_transcription)

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