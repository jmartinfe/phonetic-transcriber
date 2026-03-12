import json
from dataclasses import dataclass
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

sources = {
    "cmu" : Path("app/data/cmu_dict.json"),  # Path to the CMU Pronouncing Dictionary JSON file
    "es_transcriptions" : Path("app/data/es_transcription.json")  # Path to the Spanish transcription JSON file
}

BUILD_DIR = Path("app/build") # Path to the folder where compiled files are stored
ES_COMPILED_DICTIONARY_PATH = BUILD_DIR / "es_compiled_dictionary.json"  # Path to save the compiled dictionary JSON file
ES_COMPILED_NOTES_PATH = BUILD_DIR / "es_compiled_notes.json"  # Path to save the compiled notes JSON file

@dataclass
class RuleMaps:
    transcriptions: dict
    ipa: dict
    notes: dict

def get_source_dict(source: Path) -> dict:
    """Returns dict structure based on source json file. """
    with source.open(encoding="utf-8") as f:
        return json.load(f)

def needs_rebuild():
    """ Executes compiled files if source files 
    have been modified since last compilation
    or if compiled files do not exist. """
    if not ES_COMPILED_DICTIONARY_PATH.exists() or not ES_COMPILED_NOTES_PATH.exists():
        logger.info("Compiled files not found, rebuild needed.")
        return True

    compiled_time = min(
        ES_COMPILED_DICTIONARY_PATH.stat().st_mtime,
        ES_COMPILED_NOTES_PATH.stat().st_mtime
    )
    for s in sources.values():
        if s.stat().st_mtime > compiled_time:
            logger.info(f"Source file {s} has been modified since last compilation. Rebuild needed.")
            return True

    logger.info("Compiled dictionary and notes are up to date. No rebuild needed.")
    return False

def parse_rules(transcriptions: dict) -> RuleMaps:

    trans_map = {}
    ipa_map = {}
    notes_map = {}
    """
        Build lookup maps for each phoneme rule so we can access transcription and
        IPA symbol in O(1) time during dictionary compilation.

        Example rule:
        {
            "AA0": {
                "transcription": "a",
                "ipa": "ɑ",
                "note": "Sonido \"a\" como en \"cat\""
            }
        }

        Becomes three lookup tables:
        trans_map: {"AA0": "a"}
        ipa_map: {"AA0": "ɑ"}
        notes_map: {"A": "Sonido \"a\" como en \"cat\""}
    """
    for phoneme, rule in transcriptions.items():
        transcription = rule.get("transcription", "")
        trans_map[phoneme] = transcription
        ipa = rule.get("ipa", "")
        ipa_map[phoneme] = ipa
        note = rule.get("note", "")
        if note: # Only add to notes_map if there is a note
            notes_map[transcription.upper()] = note

    for note in notes_map.values():
        if note:
            logger.debug(f"Note added: {note}")
    return RuleMaps(trans_map, ipa_map, notes_map)

def parse_pronunciations(rules: RuleMaps, cmu: dict) -> dict:
    """
        Convert each CMU dictionary pronunciation into a compiled entry
        using the transcription and IPA maps created above.

        Example CMU entry:
        {
            "AN": ["AA0 N"]
        }

        Becomes:
        {
            "AN": [
                {
                    "transcription": "an",
                    "ipa": "ɑn"
                }
            ]
        }
    """
    compiled = defaultdict(list)
    for word, prons in cmu.items():

        # Remove any parenthetical suffixes (e.g. "AN(1)" -> "AN")
        # Convert to lowercase for consistent lookup
        base_word = word.partition("(")[0].lower()  

        # Each word can have multiple pronunciations in the CMU dictionary.
        # Build one compiled entry per pronunciation.
        for pron in prons:

            phonemes = pron.split()

            transcription = []
            ipa = []

            # Build transcription and IPA for the current pronunciation
            # by iterating over its phonemes.
            for p in phonemes:
                transcription.append(
                    "[" + rules.transcriptions.get(p, "").upper() + "]" if rules.notes.get(p, "")
                    else rules.transcriptions.get(p, ""))
                ipa.append(rules.ipa.get(p, ""))

            entry = {
                "transcription": "".join(transcription),
                "ipa": "".join(ipa)
            }


            compiled[base_word].append(entry)

    return dict(compiled)

def build_dictionary():
    rules_maps = parse_rules(get_source_dict(sources["es_transcriptions"]))
    return parse_pronunciations(rules_maps, get_source_dict(sources["cmu"])) 

def compile_all():
    rules_maps = parse_rules(get_source_dict(sources["es_transcriptions"]))
    
    dictionary = parse_pronunciations(rules_maps, get_source_dict(sources["cmu"]))
    
    BUILD_DIR.mkdir(exist_ok=True)
    
    with ES_COMPILED_DICTIONARY_PATH.open("w", encoding="utf8") as f:
        json.dump(dictionary, f, ensure_ascii=False, separators=(",", ":"))
    
    with ES_COMPILED_NOTES_PATH.open("w", encoding="utf8") as f:
        json.dump(rules_maps.notes, f, ensure_ascii=False, separators=(",", ":"))

@lru_cache
def get_compiled_data():
    if needs_rebuild():
        compile_all()
    with ES_COMPILED_DICTIONARY_PATH.open(encoding="utf-8") as f:
        dictionary = json.load(f)
    with ES_COMPILED_NOTES_PATH.open(encoding="utf-8") as f:
        notes = json.load(f)
    return dictionary, notes