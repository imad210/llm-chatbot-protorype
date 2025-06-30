# backend/app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path # Import Path for robust path handling

# Load environment variables from .env file.
# It's good practice to place the .env file in the root of the 'backend' directory,
# one level up from the 'app' directory, so load_dotenv can find it.
# If your .env is in C:\Users\caket\chatbot-prototype\backend, this will find it.
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

# Define the base data directory relative to the current file (config.py).
# This makes the paths portable across different operating systems and user directories.
# Path(__file__).resolve() gives the absolute path to config.py
# .parent gives the 'app' directory
# .parent again gives the 'backend' directory
# / 'data' appends the 'data' folder name
DATA_PATH = Path(__file__).resolve().parent.parent / "data"

CSV_FILE = DATA_PATH / "cube_dashboard_portal_analitik_v3_mapped.csv"
EMBEDDINGS_FILE = DATA_PATH / "embeddings_reduced2.npy"
FAISS_INDEX_FILE = DATA_PATH / "faiss_reduced2.index"

# Retrieve OpenAI API key from environment variables.
# Ensure you have OPENAI_API_KEY set in your .env file (e.g., OPENAI_API_KEY="your_api_key_here")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verify that the necessary files exist.
# This check is crucial to ensure the application starts correctly.
# It will raise a FileNotFoundError if any required file is missing.
for file_path in [CSV_FILE, EMBEDDINGS_FILE, FAISS_INDEX_FILE]:
    if not file_path.exists(): # Use .exists() method from pathlib.Path
        raise FileNotFoundError(f"Required data file not found: {file_path}")

# Optional: Add a check for the API key as well
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

