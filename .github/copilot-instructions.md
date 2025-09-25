# Copilot Instructions for skills-matcher

## Project Overview
- This repo implements a skill matching API using FastAPI, GCP, sentence-transformers, and model2vec.
- The standardized skill database is `data/database/metadata_superSkill.json`.
- The main task is to match raw skill inputs to standardized skills using semantic similarity.

## Architecture & Data Flow
- **API Layer:** FastAPI app (to be implemented) exposes endpoints for skill matching.
- **Skill Extraction:** Use `extract_skills_from_superskill_db` in `src/utils/extract_skills.py` to load all standardized skills.
- **Matching Logic:** Place matching code in `src/core/matcher.py` using sentence-transformers and model2vec for embedding and similarity.
- **Data:** Raw skills are matched against the standardized database.
- **Cloud Integration:** GCP can be used for deployment, scaling, or storage (not yet implemented).

## Developer Workflows
- **Run Extraction:**
  ```zsh
  python main.py
  ```
- **Start API (example):**
  ```zsh
  uvicorn api:app --reload
  ```
- **Dependencies:** Managed via `pyproject.toml` and `uv.lock`. Use [uv](https://github.com/astral-sh/uv) for Python package management.
- **Python Version:** Requires Python 3.12+.
- **Testing:** Add tests in `data/test/`.

## Conventions & Patterns
- **Imports:** Use absolute imports (e.g., `from src.utils.extract_skills import ...`).
- **Utilities:** Place reusable functions in `src/utils/`.
- **Core Logic:** Place matching and processing logic in `src/core/`.
- **API:** Place FastAPI app in `api.py` or `src/api/`.
- **Data Files:** All persistent data should be stored in `data/`.
- **Output:** Write results to text files for downstream use.

## Integration Points
- **External Libraries:**
  - FastAPI for API endpoints
  - sentence-transformers and model2vec for skill embedding and matching
  - torch/torchvision for model support
- **Cloud:** GCP integration for deployment or storage (future)
- **Custom Indexes:** PyTorch dependencies use a custom CPU index (see `pyproject.toml`).

## Example Workflow
- Extract standardized skills:
  ```python
  from src.utils.extract_skills import extract_skills_from_superskill_db
  skills = extract_skills_from_superskill_db("./data/database/metadata_superSkill.json")
  ```
- Match raw skills:
  ```python
  # Use sentence-transformers/model2vec to embed raw and standardized skills, then match by similarity
  ```

## Key Files & Directories
- `main.py`: Entrypoint for extraction
- `src/utils/extract_skills.py`: Skill extraction utility
- `src/core/matcher.py`: Skill matching logic (to be implemented)
- `data/database/metadata_superSkill.json`: Source database
- `pyproject.toml`: Dependency management

---
For unclear conventions or missing documentation, ask the user for clarification or examples before making assumptions.
