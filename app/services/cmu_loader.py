import json
from dataclasses import dataclass
from typing import List, Optional
from functools import lru_cache

CMU_FILE_PATH = 'data/cmu_dict.json'  # Path to the CMU Pronouncing Dictionary JSON file
ES_TRANSCRIPTION_PATH = 'data/es_transcription.json'  # Path to the Spanish transcription JSON file
ES_COMPILED_DICTIONARY_PATH = 'build/es_compiled_dictionary.json'  # Path to save the compiled dictionary JSON file
cmu_dict = None
transcription_dict = None

@dataclass
class WordTranscription:
    transcription: List[str]
    ipa: Optional[List[str]] = None
    description: Optional[str] = None

@lru_cache
def get_cmu_dict() -> dict:
    """Get the CMU Pronouncing Dictionary. """
    with open(CMU_FILE_PATH) as f:
        return json.load(f)

@lru_cache
def get_transcription() -> dict:
    """Get the Spanish transcription dictionary."""
    with open(ES_TRANSCRIPTION_PATH) as f:
        return json.load(f)

def get_word_transcription(word: str) -> list[list[str]]:
    """Get the transcription of a word using the CMU Pronouncing Dictionary and the Spanish transcription."""
    cmu_dict = get_cmu_dict()
    transcription_dict = get_transcription()

    prons = cmu_dict.get(word.upper(), [])

    results = []

    for pron in prons:
        phonemes = pron.split()

        results.append([
            transcription_dict.get(p, {}).get("transcription", "")
            for p in phonemes
        ])

    return results

def build_compiled_dictionary():
    cmu = get_cmu_dict()
    rules = get_transcription()

    trans_map = {}
    ipa_map = {}
    desc_map = {}

    for phoneme, rule in rules.items():
        trans_map[phoneme] = rule.get("transcription", "")
        ipa_map[phoneme] = rule.get("ipa", "")
        desc_map[phoneme] = rule.get("description")

    compiled = {}

    for word, prons in cmu.items():

        entries = []

        for pron in prons:

            phonemes = pron.split()

            transcription = []
            ipa = []
            descriptions = set()

            for p in phonemes:

                transcription.append(trans_map.get(p, ""))
                ipa.append(ipa_map.get(p, ""))

                desc = desc_map.get(p)
                if desc:
                    descriptions.add(desc)

            entry = {
                "transcription": transcription,
                "ipa": ipa
            }

            if descriptions:
                entry["description"] = ". ".join(sorted(descriptions))

            entries.append(entry)

        compiled[word] = entries

    return compiled

def save_compiled_dictionary():
    compiled = build_compiled_dictionary()

    with open(ES_COMPILED_DICTIONARY_PATH, "w", encoding="utf8") as f:
        json.dump(compiled, f, ensure_ascii=False, separators=(",", ":"))