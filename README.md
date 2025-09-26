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


## API Endpoints & Usage

### `/match-skills`
**POST**: Match a list of raw skills to standardized super skills.
**Payload:**
```json
{
	"skills": ["python", "aws", "sql"]
}
```
**Response:**
```json
{
	"results": [
		{"_id": 0, "skillId": "python", "superSkillId": [{"elId": ..., "value": ...}]},
		...
	]
}
```

### `/match-skills-file`
**POST**: Upload Excel/CSV file, returns same file with mapped skills column.
**File:** `.csv` or `.xlsx` (skills in first column)
**Response:** Downloadable file with columns: `_id`, `skill_raw`, `skill_super` (array)


### `/mappings`
**POST**: Flexible skill-to-super-skill matching for user data.
**Payload:**
Supports:
- Single skill string: `{ "skillId": "python" }`
- Skill object: `{ "skillId": {"id": 12, "value": "python"} }`
- List of skill strings: `{ "skillId": ["python", "sql"] }`
- List of skill objects: `{ "skillId": [{"id": 12, "value": "python"}, {"id": 13, "value": "SQL"}] }`
- Custom super-skills: `superSkillId` as flat list or dict-of-objects list

**Custom superSkillId examples:**
```json
"superSkillId": [
	{"elId": 123, "value": "Python"},
	{"elId": 456, "value": "AWS"}
]
```
or
```json
"superSkillId": [
	{"1": {"elId": 1, "value": "3D", "frequency": 1}, "2": {"elId": 2, "value": "Bluetooth", "frequency": 46}}
]
```

**Response:**
```json
{
	"results": [
		{"skillId": "python", "superSkillId": [{"elId": ..., "value": ...}]},
		...
	]
}
```

### `/mappings-to-file`
**POST**: Flexible skill-to-super-skill matching for user data, returns a downloadable file (CSV or XLSX) with mapping results.
**Payload:**
Same as `/mappings`, plus optional `file_type` ("csv" or "xlsx", default: "csv"):
```json
{
	"skillId": ["python", "sql"],
	"superSkillId": [
		{"elId": 123, "value": "Python"},
		{"elId": 456, "value": "AWS"}
	],
	"file_type": "csv"
}
```
**Response:**
Downloadable file with columns:
- `_id`: Row index
- `skill_raw`: Input skill value
- `skill_super`: Array of matched super skills

File format matches `/match-skills-file` output. Set `file_type` to "xlsx" for Excel output.

## Integration Points
- FastAPI, sentence-transformers, model2vec, torch, torchvision
- GCP for deployment (future)

---
For more details, see `.github/copilot-instructions.md`.
