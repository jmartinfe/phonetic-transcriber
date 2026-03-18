from app.services.transcription_service import TranscriptionService
from app.loaders.cmu_loader import get_compiled_data

dictionary_data = get_compiled_data()
transcription_service = TranscriptionService(dictionary_data)

def get_transcription_service() -> TranscriptionService:
    return transcription_service