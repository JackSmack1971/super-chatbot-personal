# AGENTS.md: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency, maintain code quality, and optimize agent performance.

*Generated from Personal Propositional RAG System - Research-Validated Implementation*

## 1. Project Overview & Purpose

*   **Primary Goal:** Transform personal document collections into an intelligent, conversational knowledge base using research-validated propositional retrieval for surgical precision in fact extraction and citation, implementing Dense X Retrieval insights for academic-quality source attribution.
*   **Business Domain:** AI/ML Research, Personal Productivity, Knowledge Management, Retrieval-Augmented Generation (RAG) Systems.
*   **Key Features:** Proposition-level fact extraction, span-based precise citations, BGE embedding optimization, cost-efficient personal RAG, academic-quality source attribution, real-time document processing through chat interface.

## 2. Core Technologies & Stack

*   **Languages:** Python 3.11+ (primary development language)
*   **Frameworks & Runtimes:** LangChain (propositional-retrieval template), Gradio 4.0+ (ChatInterface), sentence-transformers (BGE embeddings)
*   **Databases:** Pinecone Serverless (384-dimensional vector storage with rich metadata)
*   **Key Libraries/Dependencies:** 
    *   `gradio>=4.0.0` (multimodal chat interface)
    *   `pinecone-client>=3.0.0` (384-dim serverless support)
    *   `sentence-transformers>=2.2.2` (BGE-small-en-v1.5 embeddings)
    *   `openai>=1.0.0` (OpenRouter API compatibility)
    *   `langchain>=0.1.0` (propositional template scaffolding)
    *   `pypdf2>=3.0.0`, `python-docx>=0.8.11` (document processing)
*   **Platforms:** Local development, cloud deployment ready (AWS us-west-2 for Pinecone)
*   **Package Manager:** pip (Python standard package manager)
*   **External APIs:** OpenRouter API (300+ LLM models with automatic fallbacks), Pinecone Serverless (vector database)

## 3. Architectural Patterns & Structure

*   **Overall Architecture:** Research-validated Propositional RAG system implementing Dense X Retrieval methodology. The architecture separates document propositionization (LLM-based fact extraction) from retrieval (BGE embeddings + Pinecone) and generation (OpenRouter models), enabling surgical precision in citation and fact attribution.
*   **Directory Structure Philosophy:**
    *   `/src`: Contains all primary source code for propositionization, retrieval, and chat interface
    *   `/tests`: Contains unit and integration tests with 30-50 Q/A evaluation dataset
    *   `/docs`: Project documentation including research findings and performance benchmarks
    *   `/config`: Configuration files for API keys, model settings, and deployment parameters
*   **Module Organization:** Feature-based structure with separate modules for propositionization pipeline, embedding generation, vector storage interface, citation system, and Gradio chat interface. Each module handles a specific aspect of the propositional RAG workflow.
*   **Common Patterns & Idioms:**
    *   **Research Validation:** All technical decisions backed by 2025 research (Dense X Retrieval, BGE performance studies)
    *   **Cost Optimization:** Batch processing, content hashing, automatic model fallbacks to minimize API costs
    *   **Quality Validation:** Span-based citation tracking, confidence scoring, proposition-to-source mapping verification
    *   **Propositionization:** LLM-based atomic fact extraction with "no new facts" constraints
    *   **Context Management:** Parent context expansion for improved answer coherence

## 4. Coding Conventions & Style Guide

*   **Formatting:** Follow PEP 8 Python standards. Use Black for automatic formatting. Max line length: 100 characters. Use type hints for all function signatures and class definitions.
*   **Naming Conventions:**
    *   Variables, functions, methods: `snake_case` (e.g., `proposition_text`, `extract_facts()`)
    *   Classes: `PascalCase` (e.g., `PropositionExtractor`, `CitationManager`)
    *   Constants: `SCREAMING_SNAKE_CASE` (e.g., `MAX_PROPOSITION_LENGTH`, `DEFAULT_CONFIDENCE_THRESHOLD`)
    *   Files: `snake_case` (e.g., `proposition_pipeline.py`, `citation_system.py`)
*   **API Design Principles:** 
    *   **Research-Backed:** All APIs implement patterns validated by Dense X Retrieval research
    *   **Cost-Conscious:** APIs designed for batch processing and minimal external calls
    *   **Quality-First:** Built-in validation for proposition quality and citation accuracy
    *   **Extensible:** Modular design enables easy model upgrades (BGE-small to BGE-M3, OpenRouter model switching)
*   **Documentation Style:** All public functions and classes **MUST** have comprehensive docstrings explaining purpose, parameters, return values, and research validation where applicable. Use Google-style docstrings.
*   **Error Handling:** Use custom exceptions for business logic errors (`PropositionExtractionError`, `CitationMappingError`). Implement retry logic with exponential backoff for API calls. Use `assert` for precondition checking in development.
*   **Forbidden Patterns:** 
    *   **NEVER** hardcode API keys or secrets - use environment variables exclusively
    *   **NEVER** bypass span validation for propositions - 95%+ mapping accuracy required
    *   **NEVER** make unbatched API calls for large document processing - optimize for cost efficiency

## 5. Development & Testing Workflow

*   **Local Development Setup:**
    1. Install Python 3.11+ and create virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
    2. Install dependencies: `pip install -r requirements.txt`
    3. Set up environment variables: Copy `.env.example` to `.env` and configure OpenRouter API key and Pinecone credentials
    4. Download BGE-small-en-v1.5 model: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"`
    5. Initialize Pinecone index: `python scripts/setup_pinecone.py`
    6. Start Gradio interface: `python src/main.py`

*   **Build Commands:**
    *   Development server: `python src/main.py`
    *   Batch document processing: `python scripts/batch_propositionize.py`
    *   Model validation: `python scripts/validate_embeddings.py`

*   **Testing Commands:** **Every new feature requires corresponding tests with research validation.**
    *   Run all tests: `pytest tests/ -v`
    *   Run proposition quality tests: `pytest tests/test_proposition_quality.py`
    *   Run citation accuracy tests: `pytest tests/test_citation_system.py`
    *   Run performance benchmarks: `python tests/benchmark_vs_baseline.py`
    *   **CRITICAL:** All tests **MUST** mock OpenRouter and Pinecone APIs to prevent external costs during testing

*   **Linting/Formatting Commands:** **All code MUST pass formatting and type checking.**
    *   Format code: `black src/ tests/ scripts/`
    *   Check typing: `mypy src/`
    *   Lint code: `flake8 src/ tests/`
    *   Run all checks: `python scripts/check_code_quality.py`

*   **CI/CD Process Overview:** Automated testing and quality checks run on every commit. Tests must pass, code must be formatted, and performance benchmarks must show ≥15% improvement over baseline before merging.

## 6. Git Workflow & PR Instructions

*   **Pre-Commit Checks:** **ALWAYS** run `python scripts/check_code_quality.py` and ensure all tests pass before committing. Verify no API keys are committed and cost monitoring is functional.
*   **Branching Strategy:** Work on feature branches named `feat/proposition-extraction` or `fix/citation-accuracy`. **DO NOT** commit directly to `main` branch.
*   **Commit Messages:** Follow Conventional Commits specification:
    *   `feat: implement span-based citation tracking`
    *   `fix: resolve proposition extraction timeout issues`
    *   `docs: update research validation documentation`
    *   `perf: optimize batch proposition processing for cost efficiency`
*   **Pull Request (PR) Process:**
    1. Ensure branch is up-to-date with `main` and all conflicts resolved
    2. Verify all quality gates pass (tests, linting, performance benchmarks)
    3. Include performance metrics in PR description (citation accuracy, cost per document)
    4. Add research references for any new technical approaches
*   **Force Pushes:** **NEVER** use `git push --force` on `main` branch. Use `git push --force-with-lease` only on personal feature branches when necessary.
*   **Clean State:** **You MUST leave the repository in a clean state** - no uncommitted changes, no API keys exposed, no temporary files, no cached model artifacts in git.

## 7. Security Considerations

*   **General Security Practices:** **Be highly security-conscious** when handling document processing and external API integrations. Generate secure code that prevents injection attacks and data leakage.
*   **Sensitive Data Handling:** **DO NOT** hardcode any OpenRouter API keys, Pinecone credentials, or other secrets. All sensitive data **MUST** be loaded from environment variables or secure configuration files excluded from version control.
*   **Input Validation:** **ALWAYS** validate and sanitize all document inputs and user queries to prevent injection attacks or malicious content processing.
*   **Vulnerability Avoidance:** Prevent common vulnerabilities including:
    *   Code Injection (CWE-94) - validate all dynamic code execution
    *   OS Command Injection (CWE-78) - sanitize file paths and external commands
    *   Missing Authentication (CWE-306) - implement proper API authentication
    *   Data Exposure (CWE-200) - ensure personal documents aren't logged or cached inappropriately
*   **Dependency Management:** Regularly update dependencies to mitigate known vulnerabilities. Monitor for security advisories on OpenRouter and Pinecone integrations.
*   **Principle of Least Privilege:** Ensure OpenRouter and Pinecone API keys have minimal required permissions. Implement proper access controls for document processing.

## 8. Specific Agent Instructions & Known Issues

*   **Cost Monitoring:** **CRITICAL** - Monitor OpenRouter and Pinecone usage in real-time. Set budget alerts at $150/month. Implement automatic cost optimization through batch processing and model fallbacks.

*   **Quality Assurance & Verification:** After making any changes:
    *   **MUST** run full test suite and ensure 95%+ citation accuracy maintained
    *   **MUST** validate proposition-to-source span mapping accuracy
    *   **MUST** verify 15-30% performance improvement over baseline RAG system
    *   **MUST** check that confidence scores are properly calibrated

*   **Research Validation Requirements:**
    *   All new approaches **MUST** reference Dense X Retrieval research or equivalent validation
    *   Performance claims **MUST** be backed by statistical testing against evaluation dataset
    *   Technical decisions **MUST** consider cost optimization and academic-quality citation requirements

*   **Tool Usage:**
    *   **OpenRouter API:** Use automatic model fallbacks (primary: `anthropic/claude-3-haiku`, fallbacks: `openai/gpt-3.5-turbo`, `meta-llama/llama-3.1-8b-instruct`)
    *   **BGE Embeddings:** Always use BGE-small-en-v1.5 for consistency unless explicitly upgrading to BGE-M3
    *   **Pinecone:** Use serverless indexing with 384-dimensional vectors and rich metadata schema

*   **Project-Specific Patterns:**
    *   **Propositionization:** Always implement "no new facts" constraint - only rewrite existing text spans into atomic facts
    *   **Citation System:** Every proposition **MUST** track character spans for precise source attribution
    *   **Context Management:** Implement parent context expansion for better answer coherence while maintaining precise citations

*   **Performance Optimization:**
    *   Target p95 response time ≤3.5s for complete pipeline
    *   Batch process documents to minimize API costs
    *   Implement content hashing to avoid reprocessing identical documents
    *   Use proposition clustering for related fact grouping

*   **Troubleshooting & Debugging:**
    *   For API failures, check OpenRouter model availability and implement graceful fallbacks
    *   For citation accuracy issues, validate span mapping algorithm and source text preprocessing
    *   For performance degradation, profile proposition extraction pipeline and optimize batch sizes
    *   **Always** provide full error traces for debugging - never truncate stack traces

*   **Context Management:** For large document collections or complex queries:
    *   Break processing into smaller batches to manage cost and memory
    *   Implement incremental indexing for new documents
    *   Use proposition confidence scores to filter low-quality extractions
    *   Create detailed performance reports for optimization recommendations

**Research Foundation:** This project implements cutting-edge propositional RAG based on Dense X Retrieval research. All technical decisions are validated against 2025 research findings. Maintain this research-backed approach in all modifications and extensions.
