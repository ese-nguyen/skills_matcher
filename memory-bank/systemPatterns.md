# System Patterns

- API Layer: FastAPI exposes endpoints for skill mapping and file upload
- Skill Extraction: Utility loads skills from superskill database (JSON)
- Matching Logic: Uses sentence-transformers/model2vec for embeddings and similarity
- Data Model: Skill, SuperSkill, Mapping (one skill → many super-skills)
- Config: Centralized config class for all parameters
- Output: JSON and Excel export
- Error Handling: 4xx for validation, 409 for duplicates
- Containerization: Dockerfile, .env for environment
- Cloud: GCP deployment, MongoDB integration (pending)
