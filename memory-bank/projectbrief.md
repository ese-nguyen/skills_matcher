# Project Brief: Skills ↔ Super-Skills Mapping API

## Goal
Build a production-minded Python API that ingests raw skills, maps them to canonical super-skills, and exports mapped examples to Excel. Focus on clean code, pragmatic design, and thoughtful trade-offs (accuracy, performance, DX).

## Tech Stack
- Python (FastAPI, pandas, sentence-transformers, model2vec)
- Database: MongoDB (recommended), PostgreSQL (optional)
- Containerization: Docker
- Cloud: GCP (recommended)

## Key Requirements
- REST API for skill mappings (one skill → multiple super-skills)
- POST /mappings: upsert { skillId, Array[superSkillId] }
- Data model: Skill, SuperSkill, Mapping
- No duplicate skills (normalized)
- Uniqueness enforced at DB level
- Validation & error handling (4xx, 409)
- Dockerized API, .env config, GCP deploy
- Excel export with mapped samples
- README, API docs, DB schema note

## Evaluation
- Mapping correctness, completeness, code quality, validation, query efficiency, documentation
