# Skills Matcher API

## Overview
This project provides a skill matching API using FastAPI, GCP, sentence-transformers, and model2vec. It matches raw skill inputs to a standardized skill database for downstream applications.

## Architecture
- **Database:** Standardized skills are stored in `data/database/metadata_superSkill.json`.
- **Extraction:** Utilities in `src/utils/` extract all skills from the database.
- **Matching:** Core logic in `src/core/` (matcher.py) will use sentence-transformers and model2vec to embed and match skills.
- **API:** FastAPI app exposes endpoints for skill matching (to be implemented).
- **Cloud:** GCP integration for deployment and scaling (future).

## Developer Workflow
1. **Install dependencies:**
	```zsh
	uv pip install -r pyproject.toml
	```
2. **Extract skills:**
	```zsh
	python main.py
	```
3. **Run API server:**
	```zsh
	uvicorn api:app --reload
	```
4. **Add tests:** Place test scripts in `data/test/`.

## Matching Logic
- Use sentence-transformers/model2vec to embed both raw and standardized skills.
- Compute similarity and return best matches via API.

## Key Files
- `main.py`: Entrypoint for extraction
- `src/utils/extract_skills.py`: Skill extraction utility
- `src/core/matcher.py`: Skill matching logic
- `data/database/metadata_superSkill.json`: Source database
- `pyproject.toml`: Dependency management

## Example Usage
```python
from src.utils.extract_skills import extract_skills_from_superskill_db
skills = extract_skills_from_superskill_db("./data/database/metadata_superSkill.json")
# Use matcher to match raw skills to standardized skills
```

## Integration Points
- FastAPI, sentence-transformers, model2vec, torch, torchvision
- GCP for deployment (future)

---
For more details, see `.github/copilot-instructions.md`.
