class Config:
    # Paths
    SKILLS_FILE_PATH = "./data/skills.txt"
    EMBEDDINGS_CACHE_PATH = "./data/skills_embeddings.pt"
    SUPERSKILL_DB_PATH = "./data/database/metadata_superSkill.json"
    # Model
    MODEL2VEC_NAME = "minishlab/potion-multilingual-128M"
    # Matching
    SIMILARITY_THRESHOLD = 0.4
    TOP_K = 3
