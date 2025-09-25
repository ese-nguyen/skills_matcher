# Matcher logic for skill matching
import os
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding
from ..utils.extract_skills import extract_skills_from_superskill_db


# Configurable parameters
SKILLS_FILE_PATH = "./data/skills.txt"
EMBEDDINGS_CACHE_PATH = "./data/skills_embeddings.pt"
SUPERSKILL_DB_PATH = "./data/database/metadata_superSkill.json"
MODEL2VEC_NAME = "minishlab/potion-multilingual-128M"
SIMILARITY_THRESHOLD = 0.4
TOP_K = 3


def load_model():
	"""Load and return the sentence-transformers model (model2vec static embedding)."""
	static_embedding = StaticEmbedding.from_model2vec(MODEL2VEC_NAME)
	model = SentenceTransformer(modules=[static_embedding])
	return model


def generate_embeddings(skills_list, model, embeddings_cache_path):
	skills_embeddings = model.encode(skills_list, convert_to_tensor=True)
	torch.save(skills_embeddings, embeddings_cache_path)
	return skills_embeddings

def load_embeddings(skills_list, model, embeddings_cache_path):
	if os.path.exists(embeddings_cache_path):
		return torch.load(embeddings_cache_path)
	else:
		return generate_embeddings(skills_list, model, embeddings_cache_path)

def match_skills(raw_skills, model, top_k=TOP_K):
	"""
	Match a list of raw skills to standardized super skills using the provided model.
	"""
	all_skills = extract_skills_from_superskill_db(SUPERSKILL_DB_PATH)
	all_skill_values = [s['value'] for s in all_skills]
	all_skills_embeddings = load_embeddings(all_skill_values, model, EMBEDDINGS_CACHE_PATH)

	results = []
	for idx, skill in enumerate(raw_skills):
		# Exact match (case-insensitive)
		exact_matches = [s for s in all_skills if skill.lower() == s['value'].lower()]
		if exact_matches:
			super_skill_objs = [{"elId": exact_matches[0]["elId"], "value": exact_matches[0]["value"]}]
		else:
			# Similarity search
			skill_embedding = model.encode([skill], convert_to_tensor=True)
			similarities = torch.nn.functional.cosine_similarity(all_skills_embeddings, skill_embedding)
			# Get top K indices and scores
			top_k_scores, top_k_indices = torch.topk(similarities, k=top_k)
			# Filter by threshold
			filtered = [
				(score.item(), idx.item())
				for score, idx in zip(top_k_scores, top_k_indices)
				if score.item() > SIMILARITY_THRESHOLD
			]
			if filtered:
				super_skill_objs = [
					{"elId": all_skills[idx]["elId"], "value": all_skills[idx]["value"]}
					for _, idx in filtered
				]
			else:
				# If none above threshold, return the highest
				best_idx = top_k_indices[0].item()
				super_skill_objs = [{"elId": all_skills[best_idx]["elId"], "value": all_skills[best_idx]["value"]}]
		results.append({
			"_id": idx,
			"skillId": skill,
			"superSkillId": super_skill_objs
		})
	return results
