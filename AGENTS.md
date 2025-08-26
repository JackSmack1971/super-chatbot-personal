# AGENTS.md: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency, maintain code quality, and optimize agent performance.

*It is Tuesday, August 26, 2025. This guide is optimized for clarity, efficiency, and maximum utility for modern AI coding agents like OpenAI's Codex, GitHub Copilot Workspace, and Claude.*

*This file should be placed at the root of your repository. More deeply-nested AGENTS.md files (e.g., in subdirectories) will take precedence for specific sub-areas of the codebase. Direct user prompts will always override instructions in this file.*

## 1. Project Overview & Purpose

*   **Primary Goal:** A modern machine learning web application framework built with Gradio 5 for creating real-time ML demos and interactive interfaces, with custom components and production-ready deployment capabilities.
*   **Business Domain:** Machine Learning, Artificial Intelligence, Web Application Development, Interactive Data Science.
*   **Key Features:** Real-time model inference, streaming audio/video processing, custom UI components, WebRTC integration, production authentication, multi-user concurrent processing.

## 2. Core Technologies & Stack

*   **Languages:** Python 3.10+, TypeScript 5.2+, JavaScript ES2023, HTML5, CSS3.
*   **Frameworks & Runtimes:** Gradio 5.x, Node.js 18+ LTS ("Hydrogen"), FastAPI (for custom API endpoints), PyTorch/TensorFlow (ML backends).
*   **Databases:** Redis (for session caching and queue management), PostgreSQL (user data and analytics).
*   **Key Libraries/Dependencies:** 
    *   Python: `gradio>=5.0.0`, `fastapi`, `uvicorn`, `redis-py`, `torch`, `numpy`, `pandas`, `pillow`
    *   Node.js: Custom Gradio components with `gradio cc`, `typescript`, `vite`, `tailwindcss`
*   **Package Manager:** `uv` (Python dependency management), `npm 9+` (Node.js components).
*   **Platforms:** Linux (primary deployment), Docker containers, Web browsers (Chrome, Firefox, Safari, Edge).

## 3. Architectural Patterns & Structure

*   **Overall Architecture:** Hybrid Python-Node.js architecture with Gradio 5 as the primary web framework. Python backend handles ML inference and API logic, while Node.js manages custom component development and build processes. Uses event-driven patterns for real-time streaming and WebRTC for low-latency communication.
*   **Directory Structure Philosophy:**
    *   `/src`: All primary Python source code including models, services, and Gradio interfaces
    *   `/components`: Custom Gradio components built with Node.js/TypeScript
    *   `/tests`: Unit and integration tests parallel to source structure
    *   `/config`: Application configurations, environment files, and deployment settings
    *   `/static`: Static assets including CSS, images, and pre-built components
    *   `/docs`: Technical documentation and API references
*   **Module Organization:** 
    *   Python: Feature-based modules (`src/audio/`, `src/vision/`, `src/text/`) with shared utilities in `src/common/`
    *   Node.js: Component-based structure with each custom component in separate directories under `/components`
    *   Gradio interfaces organized by functionality with shared layouts in `src/interfaces/shared/`
*   **Common Patterns & Idioms:**
    *   **Async Processing:** Heavy use of `async/await` for ML inference and streaming operations
    *   **Streaming Architecture:** Generator functions with `yield` for progressive result display
    *   **Component Composition:** Reusable Gradio blocks and custom components for consistent UI
    *   **State Management:** `gr.State` for user session data with Redis backing for persistence
    *   **Error Boundaries:** Comprehensive error handling with user-friendly fallbacks

## 4. Coding Conventions & Style Guide

*   **Formatting:** 
    *   Python: Follow PEP 8, use Black formatter with 88-character line limit, isort for imports
    *   TypeScript/JavaScript: Prettier with 2-space indentation, single quotes, trailing commas, 100-character line limit
    *   Use `.editorconfig` for consistent formatting across editors
*   **Naming Conventions:**
    *   Python: `snake_case` for variables, functions, files; `PascalCase` for classes; `SCREAMING_SNAKE_CASE` for constants
    *   TypeScript: `camelCase` for variables, functions; `PascalCase` for components, types, interfaces; `kebab-case` for CSS classes
    *   Files: Python modules use `snake_case.py`, TypeScript components use `PascalCase.tsx`
*   **API Design Principles:** 
    *   RESTful design for FastAPI endpoints with clear resource naming
    *   Gradio interfaces designed for immediate usability with sensible defaults
    *   Custom components expose minimal, type-safe APIs with comprehensive JSDoc documentation
    *   Prioritize streaming and real-time capabilities over batch processing where appropriate
*   **Documentation Style:** 
    *   Python: Comprehensive docstrings using Google style for all public functions and classes
    *   TypeScript: JSDoc comments for all exported functions, types, and components
    *   Always document parameter types, return values, and expected exceptions
*   **Error Handling:** 
    *   Python: Use custom exception classes inheriting from `GradioError`, proper async exception handling
    *   TypeScript: Return `Result<T, Error>` types for fallible operations, avoid throwing in component lifecycle
    *   Always provide user-friendly error messages in Gradio interfaces
*   **Forbidden Patterns:** 
    *   **NEVER** use `any` type in TypeScript without explicit justification
    *   **DO NOT** use synchronous file operations in Node.js/Python async contexts
    *   **AVOID** blocking the event loop with CPU-intensive operations (use worker threads/processes)
    *   **NEVER** hardcode API keys, model paths, or sensitive configuration

## 5. Development & Testing Workflow

*   **Local Development Setup:**
    1. **Install Python 3.10+** and `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    2. **Install Node.js 18+ LTS**: Use nvm or direct download from nodejs.org
    3. **Python environment**: `uv venv` then `uv pip install -r requirements.txt`
    4. **Node.js dependencies**: `npm install` (for custom components)
    5. **Start development**: `uv run python app.py` (main Gradio app), `npm run dev` (component development)
*   **Build Commands:**
    *   Python app: `uv run python -m src.main` (production mode)
    *   Custom components: `cd components && npm run build`
    *   Docker build: `docker build -t gradio-app .`
*   **Testing Commands:** **All commits require corresponding unit tests.**
    *   Python tests: `uv run pytest tests/ -v --cov=src`
    *   Node.js tests: `npm test` (runs Vitest with coverage)
    *   Integration tests: `uv run pytest tests/integration/ --slow`
    *   **CRITICAL**: All tests **MUST** mock external services (ML APIs, file systems) using `pytest-mock`, `responses`, or Vitest mocking
    *   Test filenames: Python `test_*.py`, TypeScript `*.test.ts`
*   **Linting/Formatting Commands:** **All code MUST pass linting before committing.**
    *   Python: `uv run black . && uv run isort . && uv run flake8 src tests`
    *   TypeScript: `npm run lint:fix && npm run type-check`
    *   Security scanning: `uv run bandit -r src` and `npm audit`
*   **CI/CD Process Overview:** GitHub Actions automatically runs all tests, linters, security scans, and builds Docker images on every pull request. Integration tests run against staging environment. Nothing merges to `main` unless all checks pass.

## 6. Git Workflow & PR Instructions

*   **Pre-Commit Checks:** **ALWAYS** run `make check` (runs all linters, formatters, and fast tests) before committing. Install pre-commit hooks: `uv run pre-commit install`
*   **Branching Strategy:** 
    *   Work on feature branches named `feat/description` or `fix/description`
    *   **DO NOT** commit directly to `main` or `develop` branches
    *   Use `git checkout -b feat/your-feature` for new work
*   **Commit Messages:** Follow Conventional Commits specification:
    *   `feat: add real-time audio processing component`
    *   `fix: resolve memory leak in streaming video handler`
    *   `docs: update API documentation for custom components`
    *   Each commit message **MUST** answer: What changed? Why? Breaking changes? Dependencies updated?
*   **Pull Request (PR) Process:**
    1. Ensure branch is up-to-date: `git rebase main`
    2. Verify all tests pass: `make test-all`
    3. Update documentation if needed
    4. Create PR with clear title and description linking to relevant issues
    5. Add appropriate labels: `gradio`, `nodejs`, `security`, `performance`
*   **Force Pushes:** **NEVER** use `git push --force` on shared branches. Use `git push --force-with-lease` only on personal feature branches when absolutely necessary.
*   **Clean State:** **You MUST leave your worktree in a clean state after completing a task.** No untracked files, no uncommitted changes, no temporary build artifacts.

## 7. Security Considerations

*   **General Security Practices:** **Be extremely security-conscious when handling user uploads, model inputs, and external API integrations.** Generate secure code that prevents OWASP Top 10 vulnerabilities.
*   **Sensitive Data Handling:** 
    *   **DO NOT** hardcode API keys, model paths, or secrets anywhere in code
    *   Use environment variables loaded from `.env` files (never committed)
    *   Store sensitive config in secure key management systems for production
*   **Input Validation:** 
    *   **ALWAYS** validate file uploads (type, size, content) before processing
    *   Sanitize all text inputs to prevent XSS and injection attacks
    *   Use Gradio's built-in file validation features and extend with custom checks
*   **Vulnerability Avoidance:**
    *   Prevent arbitrary code execution through model inputs or file uploads
    *   Implement proper authentication and session management
    *   Use HTTPS in all production deployments with proper certificate management
    *   Regular dependency scanning with `npm audit` and `uv pip check`
*   **Principle of Least Privilege:** 
    *   Run containers with non-root users
    *   Limit file system access in Gradio with `file_access=False` in production
    *   Use minimal Docker base images (Alpine Linux when possible)

## 8. Specific Agent Instructions & Known Issues

*   **Tool Usage:**
    *   For Python dependencies: **ALWAYS** use `uv add <package>` and `uv remove <package>`, never `pip`
    *   For Node.js dependencies: Use `npm install <package>` with npm 9+ features
    *   For Gradio components: Use `gradio cc create ComponentName` and `gradio cc dev`
    *   Git operations: Use `gh` CLI for GitHub interactions when available
*   **Context Management:** 
    *   For large ML model integration tasks, break into smaller, testable PRs
    *   If context window is nearing limit, create a plan document first, then implement incrementally
    *   Focus on one component or feature at a time to maintain clarity
*   **Quality Assurance & Verification:** 
    *   After making changes, **YOU MUST** run all relevant tests and ensure they pass
    *   For Gradio interfaces, manually verify UI components render correctly
    *   For streaming features, test with realistic data sizes and concurrent users
    *   **ALWAYS** check that custom components build successfully with `npm run build`
*   **Project-Specific Quirks/Antipatterns:**
    *   Gradio 5 breaking changes: Use `max_height` instead of `height` for DataFrames
    *   Audio components now use `format=None` by default - set explicit format if needed
    *   SVG files require `type="filepath"` in Image components for security
    *   WebRTC components require `time_limit` settings to prevent resource exhaustion
*   **Troubleshooting & Debugging:** 
    *   If Gradio app fails to start, check for port conflicts (default 7860) and proxy settings
    *   For Node.js component build issues, verify Node.js version with `node --version`
    *   Memory issues: Reduce `default_concurrency_limit` and implement proper cleanup in async functions
    *   For streaming problems, check `stream_every` timing and network stability
    *   **ALWAYS** provide full stack traces and error messages when reporting issues
*   **Performance Considerations:**
    *   Set appropriate `concurrency_limit` for ML inference endpoints (typically 2-5 for GPU models)
    *   Use `async def` for all I/O-bound operations including file processing and API calls
    *   Implement proper caching strategies for expensive model operations
    *   Monitor memory usage during development - Gradio 5 apps can be memory-intensive with multiple concurrent users

## 9. Gradio 5 Specific Guidelines

*   **Interface Creation:** Use `gr.ChatInterface` for conversational AI, `gr.Blocks` for complex layouts, `gr.Interface` only for simple function wrapping
*   **Streaming Implementation:** Always set `time_limit` for streaming events in production environments to prevent queue saturation
*   **Component Configuration:** Provide clear labels, placeholders, and examples for all input components to improve UX
*   **State Management:** Use `gr.State` with Redis backing for user sessions that persist across page reloads
*   **Custom Components:** Follow Gradio CC development patterns, ensure Node.js 18+ compatibility, implement proper TypeScript types
*   **Security Settings:** Always use `file_access=False`, `auth` middleware, and validate all file uploads in production deployments