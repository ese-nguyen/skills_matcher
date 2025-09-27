import unittest
from src.utils.extract_skills import extract_skills_from_superskill_db
import os

class TestExtractSkills(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '../database/metadata_superSkill.json')
        self.embeddings_path = os.path.join(os.path.dirname(__file__), '../skills_embeddings_optimized.pt')

    def test_extract_skills_returns_list(self):
        skills = extract_skills_from_superskill_db(self.db_path)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)

    def test_skill_format(self):
        skills = extract_skills_from_superskill_db(self.db_path)
        for skill in skills:
            self.assertIsInstance(skill, str)
            self.assertTrue(skill)

    def test_top4_semantic_matches(self):
        import torch
        from sentence_transformers import SentenceTransformer
        # Prepare test data
        all_skills_list = extract_skills_from_superskill_db(self.db_path)
        all_skills_embeddings = torch.load(self.embeddings_path)
        model = SentenceTransformer('isy-thl/multilingual-e5-base-course-skill-tuned')

        # Example input
        skills_list = ["Python", "Data Analysis", "Machine Learning", "NonexistentSkill"]
        exact_matches = {}
        remaining_skills_list = []

        # Exact lowercase matching
        for skill in skills_list:
            if skill.lower() in [s.lower() for s in all_skills_list]:
                for s in all_skills_list:
                    if skill.lower() == s.lower():
                        exact_matches[skill] = s
                        break
            else:
                remaining_skills_list.append(skill)

        # Semantic context and encoding
        remaining_skills_with_context = [f"I have experience in {skill} skills" for skill in remaining_skills_list]
        remaining_embeddings = model.encode(remaining_skills_with_context, convert_to_tensor=True)
        remaining_similarities = torch.nn.functional.cosine_similarity(
            all_skills_embeddings.unsqueeze(1),
            remaining_embeddings.unsqueeze(0),
            dim=-1
        )

        # Check top 4 matches for each remaining skill
        for idx_j, sentence2 in enumerate(remaining_skills_list):
            top_k_scores, top_k_indices = torch.topk(remaining_similarities[:, idx_j], k=4)
            self.assertEqual(len(top_k_indices), 4)
            # Ensure scores are sorted descending
            self.assertTrue(all(top_k_scores[i] >= top_k_scores[i+1] for i in range(3)))
            # Ensure returned skills are strings from all_skills_list
            for i in range(4):
                original_skill = all_skills_list[top_k_indices[i]]
                self.assertIsInstance(original_skill, str)

if __name__ == "__main__":
    unittest.main()
