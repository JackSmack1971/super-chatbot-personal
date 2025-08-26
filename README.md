# Super Chatbot Personal

## Project Overview
This project aims to build a secure and reliable AI video pipeline that transforms
personal media into an intelligent knowledge base. It follows research-validated
retrieval techniques and emphasizes strong security practices to address existing
technical debt and code duplication.

## Setup Instructions
1. Install Python **3.11**.
2. Create and activate a virtual environment:
   `python3.11 -m venv .venv && source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Configure environment variables by copying `.env.example` to `.env` and
   setting values for `OPENROUTER_API_KEY`, `PINECONE_API_KEY`, and
   `PINECONE_ENVIRONMENT`.
5. Environment variables are loaded securely via `src/config/env_loader.py`,
   which validates required keys before use.
6. Start the application with `python src/main.py` after configuration.

## Contribution Guidelines
- Follow PEP 8 formatting with a maximum line length of 100 characters and keep
  functions under 30 lines.
- Use type hints and async/await for all I/O operations.
- Validate all user inputs before processing and wrap external API calls in
  retries with timeouts and custom exceptions.
- Never hardcode API keys; load them from environment variables.
- Write tests for all new code and aim for at least 80% coverage while mocking
  external services.
- Run `python scripts/check_code_quality.py` and `pytest tests/ -v` before
  committing.
- Use Conventional Commits for messages and ensure branches are up to date with
  `main`.
