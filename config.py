import os
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv()

# Required: OpenAI API Key (must be set in .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Missing OPENAI_API_KEY in .env file.")

# Optional model config
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
