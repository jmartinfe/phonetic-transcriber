from app.services.cmu_loader import compile_dictionary, needs_rebuild
from app.core.logging_config import setup_logging

setup_logging()

if __name__ == "__main__":
    if needs_rebuild():
        compile_dictionary()