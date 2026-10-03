"""
Shared LLM
"""

import os

from pathlib import Path

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


# ==========================================================
# LOAD ENV
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


# ==========================================================
# ENVIRONMENT
# ==========================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME"
)


if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env"
    )


if not MODEL_NAME:
    raise ValueError(
        "MODEL_NAME not found in .env"
    )


# ==========================================================
# SHARED LLM
# ==========================================================

llm = ChatOpenAI(

    model=MODEL_NAME,

    api_key=OPENROUTER_API_KEY,

    base_url="https://openrouter.ai/api/v1",

    temperature=0,

    max_tokens=2048
)