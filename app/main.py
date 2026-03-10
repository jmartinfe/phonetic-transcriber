from app.services.cmu_loader import compile_dictionary
from app.core.logging_config import setup_logging

setup_logging()

if __name__ == "__main__":
    compile_dictionary()