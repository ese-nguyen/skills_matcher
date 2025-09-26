
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse, StreamingResponse
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
    # Detect file type
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
        file_type = "csv"
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))
        file_type = "xlsx"
    else:
        return JSONResponse(content={"error": "Unsupported file type. Please upload .csv or .xlsx."}, status_code=400)

    # Assume skills are in first column
    skills = df.iloc[:, 0].dropna().astype(str).tolist()
    model = app.state.model

    # Extract only superSkillId array from each mapping result
    mapped_full = match_skills(skills, model)
    mapped_super = [row.get("superSkillId", []) for row in mapped_full]

    # Build output DataFrame with required columns
    out_df = pd.DataFrame({
        "_id": range(1, len(skills) + 1),
        "skill_raw": skills,
        "skill_super": mapped_super
    })

    # Return file in same format
    output = io.BytesIO()
    if file_type == "csv":
        out_df.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=mapped_skills.csv"})
    else:
        out_df.to_excel(output, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=mapped_skills.xlsx"})

# REST API for upserting skill-superSkill mappings
@app.post("/mappings")
def upsert_mapping(payload: Dict[str, Any] = Body(...)):
    """
    Upsert a mapping: { skillId, Array[superSkillId] }
    Stores in-memory for demo; replace with DB for production.
    """
    import re
    skill_input = payload.get("skillId")
    super_skill_ids = payload.get("superSkillId")

    # Helper to extract skill value
    def extract_skill_value(item):
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return item.get("value")
        return None

    # Normalize skillId: case, space, punctuation insensitive
    def normalize_skill(s):
        return re.sub(r"[\s\W]+", "", s).lower() if s else ""

    # Build list of skill values
    if isinstance(skill_input, str):
        skill_values = [skill_input]
    elif isinstance(skill_input, dict):
        val = extract_skill_value(skill_input)
        skill_values = [val] if val else []
    elif isinstance(skill_input, list):
        skill_values = [extract_skill_value(item) for item in skill_input if extract_skill_value(item)]
    else:
        return JSONResponse(content={"error": "Invalid payload: skillId must be string, dict, or list."}, status_code=400)

    if not skill_values:
        return JSONResponse(content={"error": "No valid skill values found in skillId."}, status_code=400)

    # Check for duplicate (conflict)
    for val in skill_values:
        norm_val = normalize_skill(val)
        for existing in MAPPINGS:
            if normalize_skill(existing) == norm_val:
                return JSONResponse(content={"error": f"Duplicate skill (normalized): {val}"}, status_code=409)

    model = app.state.model
    # If superSkillId is provided, embed and match against it
    if super_skill_ids is not None:
        # Support both flat list and dict-of-objects list
        def flatten_superskill_list(lst):
            flat = []
            for item in lst:
                if isinstance(item, dict) and all(isinstance(v, dict) for v in item.values()):
                    flat.extend(list(item.values()))
                elif isinstance(item, dict) and "value" in item:
                    flat.append(item)
            return flat

        custom_super_skills = flatten_superskill_list(super_skill_ids)
        custom_values = [ss["value"] for ss in custom_super_skills if "value" in ss]
        # Embed custom super-skills
        import torch
        custom_embeddings = model.encode(custom_values, convert_to_tensor=True)
        result = []
        for skill in skill_values:
            skill_emb = model.encode([skill], convert_to_tensor=True)
            similarities = torch.nn.functional.cosine_similarity(custom_embeddings, skill_emb)
            # Get top matches (all above threshold or top 1)
            threshold = 0.4
            top_indices = (similarities > threshold).nonzero(as_tuple=True)[0].tolist()
            if not top_indices:
                # fallback to best match
                top_indices = [int(torch.argmax(similarities).item())]
            matched = [custom_super_skills[i] for i in top_indices]
            result.append({"skillId": skill, "superSkillId": matched})
            MAPPINGS[skill] = matched
    else:
        # Use matcher for each skill against default database
        match_result = match_skills(skill_values, model)
        result = [{"skillId": r["skillId"], "superSkillId": r.get("superSkillId", [])} for r in match_result]
        for r in match_result:
            MAPPINGS[r["skillId"]] = r.get("superSkillId", [])

    return JSONResponse(content={"results": result})
