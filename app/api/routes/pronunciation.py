from fastapi import APIRouter
import json
from app.services.cmu_loader import get_compiled_data

dictionary, notes = get_compiled_data()

router = APIRouter(prefix="/pronunciation", tags=["pronunciation"])

@router.get("/pronunciation/{word}")
def get_pronunciation(word: str):
    return dictionary.get(word.lower())

@router.get("/health")
def health_check():
    return {"status": "ok"}