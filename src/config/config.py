class Config:
    # Paths
    SKILLS_FILE_PATH = "./data/skills.txt"
    EMBEDDINGS_CACHE_PATH = "./data/skills_embeddings_optimized.pt"
    SUPERSKILL_DB_PATH = "./data/database/metadata_superSkill.json"
    # Model
    MODEL_NAME = "isy-thl/multilingual-e5-base-course-skill-tuned"
    # Matching
    SIMILARITY_THRESHOLD = 0.4
    TOP_K = 4
