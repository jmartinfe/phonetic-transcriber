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

@router.post("/", response_model=Transcription, 
             summary="Get Phonetic Transcription for a Phrase",
             responses={
                400: {"description": "Empty text or text too long"},
                500: {"description": "Internal transcription error"}
                }
            )
def get_phrase_pronunciation(
    request: TranscriptionRequest,
    service: TranscriptionService = Depends(get_transcription_service)
):
    """
    Endpoint to get the phonetic transcription of a given English text.
    - **text**: The English text to be transcribed.
    Returns a phonetic transcription that is easier for Spanish speakers to pronounce.
    """
    return service.get_phrase_transcription(request.text)

@router.post("/formatted/",
            response_model=FormattedTextTranscription,
            summary="Get Formatted Phonetic Transcription for a Phrase",
            responses={
                400: {"description": "Empty text or text too long"},
                500: {"description": "Internal transcription error"}
                }
            )
def get_formatted_text_pronunciation(
    request: TranscriptionRequest,
    transcription_service: TranscriptionService = Depends(get_transcription_service)
) -> FormattedTextTranscription:
    """
    Endpoint to get the formatted phonetic transcription of a given English text.
    - **text**: The English text to be transcribed.
    Returns a formatted phonetic transcription, ready to be used from any frontend application.
    """
    raw_transcription = transcription_service.get_phrase_transcription(request.text)
    return transcription_to_formatted_text_transcription(raw_transcription)

@router.post("/batch",
            response_model = BatchTranscriptionResponse,
            summary="Get Batch of Phonetic Transcriptions",
            responses={
                400: {"description": "Empty text or text too long"},
                500: {"description": "Internal transcription error"}
                }
            )
def get_phrase_pronunciations(
    request_texts: BatchTranscriptionRequest,
    service: TranscriptionService = Depends(get_transcription_service)
):
    """
    Endpoint to get the phonetic transcriptions of a batch of English texts.
    - **texts**: A list of English texts to be transcribed.
    Returns a list of phonetic transcriptions that are easier for Spanish speakers to pronounce for Spanish speakers.
    """
    transcriptions = [service.get_phrase_transcription(text) for text in request_texts.texts]
    return BatchTranscriptionResponse(transcriptions=transcriptions)

@router.get("/{word}",
            response_model=Transcription,
            summary="Get Phonetic Transcription for a Single Word",
            responses={
                400: {"description": "Empty text, text too long or word has blank spaces"},
                500: {"description": "Internal transcription error"}
                }
            )
def get_word_pronunciation(
    word: str,
    service: TranscriptionService = Depends(get_transcription_service)
) -> Transcription:
    """
    Endpoint to get the phonetic transcription of a single English word.
    - **word**: The English word to be transcribed.
    Returns a phonetic transcription that is easier for Spanish speakers to pronounce.
    """
    return service.get_word_transcription(word)