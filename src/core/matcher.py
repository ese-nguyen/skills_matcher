# Matcher logic for skill matching
import os
from ..utils.fix_input_schema import fix_skill_names
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding
from ..utils.extract_skills import extract_skills_from_superskill_db
from ..config.config import Config


# Configurable parameters
SKILLS_FILE_PATH = Config.SKILLS_FILE_PATH
EMBEDDINGS_CACHE_PATH = Config.EMBEDDINGS_CACHE_PATH
SUPERSKILL_DB_PATH = Config.SUPERSKILL_DB_PATH
MODEL_NAME = Config.MODEL_NAME
SIMILARITY_THRESHOLD = Config.SIMILARITY_THRESHOLD
TOP_K = Config.TOP_K


def load_model():
	"""Load and return the sentence-transformers model (E5 tuned)."""
	model = SentenceTransformer(MODEL_NAME)
	return model


def generate_embeddings(skills_list, model, embeddings_cache_path):
	# Add semantic context to each skill for embedding
	skills_with_context = [f"I have experience in {skill} skills" for skill in skills_list]
	skills_embeddings = model.encode(skills_with_context, convert_to_tensor=True)
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
	Uses semantic context and returns top_k matches for each skill.
	"""
	all_skills = extract_skills_from_superskill_db(SUPERSKILL_DB_PATH)
	all_skill_values = [s['value'] for s in all_skills]
	all_skills_embeddings = load_embeddings(all_skill_values, model, EMBEDDINGS_CACHE_PATH)

	# Preprocess: batch skills with length < 3 and send to fix_skill_names
	short_skills_indices = [i for i, skill in enumerate(raw_skills) if len(skill.strip()) < 4]
	short_skills = [raw_skills[i] for i in short_skills_indices]
	fixed_short_skills = fix_skill_names(short_skills) if short_skills else []

	results = []
	for idx, skill in enumerate(raw_skills):
		# Use fixed skill if it was short
		if idx in short_skills_indices:
			skill_to_match = fixed_short_skills[short_skills_indices.index(idx)]
		else:
			skill_to_match = skill
		# Exact match (case-insensitive)
		exact_matches = [s for s in all_skills if skill_to_match.lower() == s['value'].lower()]
		if exact_matches:
			super_skill_objs = [{"elId": exact_matches[0]["elId"], "value": exact_matches[0]["value"]}]
		else:
			# Add semantic context to skill for embedding
			def get_top_matches(query_skill):
				skill_with_context = f"I have experience in {query_skill} skills"
				skill_embedding = model.encode([skill_with_context], convert_to_tensor=True)
				similarities = torch.nn.functional.cosine_similarity(all_skills_embeddings, skill_embedding)
				top_k_scores, top_k_indices = torch.topk(similarities, k=top_k)
				return top_k_scores, top_k_indices
			top_k_scores, top_k_indices = get_top_matches(skill_to_match)
			if top_k_scores[0].item() < 0.8 or top_k_scores[1].item() < 0.8:
				top_k_scores, top_k_indices = get_top_matches(skill_to_match.upper())
				if top_k_scores[0].item() < 0.8 or top_k_scores[1].item() < 0.8:
					top_k_scores, top_k_indices = get_top_matches(fix_skill_names([skill_to_match])[0])

			# Filter by threshold, but always return top_k
			super_skill_objs = []
			for i, idx_top in enumerate(top_k_indices):
				score = top_k_scores[i].item()
				if score >= SIMILARITY_THRESHOLD:
					super_skill_objs.append({
						"elId": all_skills[idx_top.item()]["elId"],
						"value": all_skills[idx_top.item()]["value"]
					})
			# If none above threshold, return all top_k
			if not super_skill_objs:
				super_skill_objs = [
					{"elId": all_skills[idx_top.item()]["elId"],
					 "value": all_skills[idx_top.item()]["value"]}
					for i, idx_top in enumerate(top_k_indices)
				]
		results.append({
			"_id": idx,
			"skillId": skill,
			"superSkillId": super_skill_objs
		})
	return results
