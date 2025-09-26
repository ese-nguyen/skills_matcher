# Active Context


## What Works
- Skill extraction from superskill database
- Embedding and matching logic (exact + semantic)
- FastAPI endpoints for list and file upload (CSV/XLSX)
- Config class for all parameters
- Output includes both elId and value for super-skills
- Similarity threshold logic implemented
- Dockerfile refactored for multi-stage build, robust uv install, and .venv isolation
- Docker build works even if uv.lock is missing
- API model loading now uses FastAPI startup event for warm start
- All endpoints use preloaded model for fast response

## What Needs Work
- MongoDB integration for mappings and uniqueness enforcement
- Error handling for validation and duplicate conflicts
- Dockerfile and .env setup
- GCP deployment scripts and documentation
- Excel export endpoint for mapped samples
- API documentation and DB schema note


## Next Steps
 - Modify Excel/CSV endpoint: when a user uploads an Excel/CSV file, return the same file with an additional column for mapped skills
 - Prepare for GCP deployment
 - Update API/database as needed for future requirements
