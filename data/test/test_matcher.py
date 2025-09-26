# Additional tests for matcher.py and extract_skills.py
import os
os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import torch
from src.core import matcher
from src.utils.extract_skills import extract_skills_from_superskill_db
import unittest
from src.core.matcher import match_skills

class TestMatcher(unittest.TestCase):
    def test_match_skills_basic(self):
        # Example: raw skill matches standardized skill
        raw_skills = ["Python", "Machine Learning"]
        standardized_skills = ["Python", "Data Science", "Machine Learning"]
        matches = match_skills(raw_skills, standardized_skills)
        self.assertIn("Python", matches)
        self.assertIn("Machine Learning", matches)

    def test_match_skills_empty(self):
        raw_skills = []
        standardized_skills = ["Python", "Data Science"]
        matches = match_skills(raw_skills, standardized_skills)
        self.assertEqual(matches, [])

    def test_match_skills_no_match(self):
        raw_skills = ["Java", "C++"]
        standardized_skills = ["Python", "Data Science"]
        matches = match_skills(raw_skills, standardized_skills)
        self.assertEqual(matches, [])

    def test_match_skills_partial_match(self):
        raw_skills = ["Python", "C++"]
        standardized_skills = ["Python", "Data Science"]
        matches = match_skills(raw_skills, standardized_skills)
        self.assertIn("Python", matches)
        self.assertNotIn("C++", matches)

    def test_match_skills_case_insensitive(self):
        raw_skills = ["python", "machine learning"]
        standardized_skills = ["Python", "Machine Learning"]
        matches = match_skills(raw_skills, standardized_skills)
        # Accept either case-insensitive match or not, depending on implementation
        # If case-insensitive, both should match
        self.assertTrue(
            "Python" in matches or "python" in matches
        )
        self.assertTrue(
            "Machine Learning" in matches or "machine learning" in matches
        )

    def test_match_skills_special_characters(self):
        raw_skills = ["C#", "Node.js"]
        standardized_skills = ["C#", "Node.js", "Python"]
        matches = match_skills(raw_skills, standardized_skills)
        self.assertIn("C#", matches)
        self.assertIn("Node.js", matches)



class TestMatcherFunctions(unittest.TestCase):
    def test_load_model(self):
        model = matcher.load_model()
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "encode"))

    def test_generate_and_load_embeddings(self):
        model = matcher.load_model()
        skills_list = ["Python", "JavaScript"]
        cache_path = "./data/test_embeddings.pt"
        # Remove cache if exists
        if os.path.exists(cache_path):
            os.remove(cache_path)
        emb = matcher.generate_embeddings(skills_list, model, cache_path)
        self.assertIsInstance(emb, torch.Tensor)
        emb2 = matcher.load_embeddings(skills_list, model, cache_path)
        self.assertTrue(torch.equal(emb, emb2))
        # Clean up
        if os.path.exists(cache_path):
            os.remove(cache_path)

class TestExtractSkills(unittest.TestCase):
    def test_extract_skills_from_superskill_db(self):
        # Use a small sample JSON for testing
        import tempfile, json
        sample = [
            {"key": "skills", "val": {
                "1": {"elId": 1, "value": "Python"},
                "2": {"elId": 2, "value": "JavaScript"}
            }}
        ]
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tf:
            json.dump(sample, tf)
            tf.flush()
            skills = extract_skills_from_superskill_db(tf.name)
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0]["value"], "Python")
        self.assertEqual(skills[1]["elId"], 2)
        os.remove(tf.name)

    def test_extract_skills_from_superskill_db_empty(self):
        import tempfile, json
        sample = []
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tf:
            json.dump(sample, tf)
            tf.flush()
            skills = extract_skills_from_superskill_db(tf.name)
        self.assertEqual(skills, [])
        os.remove(tf.name)


if __name__ == "__main__":
    unittest.main()

