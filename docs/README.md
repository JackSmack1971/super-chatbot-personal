# Project Overview

## Purpose
The project provides a secure AI video pipeline that converts personal media into an interactive knowledge base. It leverages research-validated retrieval methods to deliver precise, cited responses.

## Architecture
- **Propositionization**: Extracts atomic facts from media transcripts.
- **Embedding & Storage**: Generates BGE embeddings and stores vectors in Pinecone.
- **Retrieval & Generation**: Applies Dense X Retrieval methodology to fetch relevant propositions and generate answers via OpenRouter models.

## Research Basis
The retrieval strategy is informed by Dense X Retrieval research, enabling proposition-level accuracy and cost-efficient RAG. Learn more from the [Dense X Retrieval papers](https://arxiv.org/search/?query=Dense+X+Retrieval&searchtype=all).

## Security Requirements
- Never hardcode API keys; load them from environment variables.
- Validate all user inputs prior to processing.
- Wrap external API calls in retries with timeouts.
- Use try/except blocks with custom exceptions for error reporting.

## Setup Steps
1. Install Python 3.11+.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`, `PINECONE_API_KEY`, and `PINECONE_ENVIRONMENT`.
5. Start the application:
   ```bash
   python src/main.py
   ```

## Testing Commands
- Run tests with coverage enforcement:
  ```bash
  pytest --cov=src --cov-fail-under=80 tests/
  ```
- Run code quality checks:
  ```bash
  python scripts/check_code_quality.py
  ```

## Contribution Workflow
- Follow PEP 8 with functions under 30 lines and full type hints.
- Use async/await for I/O and validate inputs.
- Ensure tests cover new code (≥80% coverage) and mock external APIs.
- Run `python scripts/check_code_quality.py` and `pytest --cov=src --cov-fail-under=80 tests/ -v` before committing.
- Use Conventional Commit messages and keep branches updated with `main`.

## Future Documentation
Additional guides and references will appear in this `docs/` directory as the project evolves.
