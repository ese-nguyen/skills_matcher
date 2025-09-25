
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import pandas as pd
from .src.core.matcher import match_skills, load_model
import io
from .src.utils.extract_skills import extract_skills_from_superskill_db
# from src/core.matcher import match_skills  # To be implemented


app = FastAPI()

# Preload model at startup and store in app.state
@app.on_event("startup")
async def startup_event():
    app.state.model = load_model()

# Load standardized skills (for demo, load once)
SUPERSKILL_DB_PATH = "./data/database/metadata_superSkill.json"
superskills = extract_skills_from_superskill_db(SUPERSKILL_DB_PATH)

# In-memory mapping store (replace with DB for production)
MAPPINGS = {}

# Dummy matcher stub (replace with real embedding/similarity logic)
## Use matcher.match_skills for real matching


@app.post("/match-skills")
def match_skills_api(skills: List[str]):
    """Match a list of raw skills to standardized super skills."""
    model = app.state.model
    mapped = match_skills(skills, model)
    return JSONResponse(content={"results": mapped})


@app.post("/match-skills-file")
def match_skills_file(file: UploadFile = File(...)):
    """Match skills from uploaded Excel/CSV file."""
    content = file.file.read()
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))
    else:
        return JSONResponse(content={"error": "Unsupported file type. Please upload .csv or .xlsx."}, status_code=400)
    # Assume skills are in first column
    skills = df.iloc[:, 0].dropna().astype(str).tolist()
    model = app.state.model
    mapped = match_skills(skills, model)
    return JSONResponse(content={"results": mapped})

# REST API for upserting skill-superSkill mappings
@app.post("/mappings")
def upsert_mapping(payload: Dict[str, Any] = Body(...)):
    """
    Upsert a mapping: { skillId, Array[superSkillId] }
    Stores in-memory for demo; replace with DB for production.
    """
    skill_id = payload.get("skillId")
    super_skill_ids = payload.get("superSkillId", [])
    if not skill_id or not isinstance(super_skill_ids, list):
        return JSONResponse(content={"error": "Invalid payload"}, status_code=400)
    MAPPINGS[skill_id] = super_skill_ids
    return JSONResponse(content={"skillId": skill_id, "superSkillId": super_skill_ids})
