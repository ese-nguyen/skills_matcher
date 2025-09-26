import unittest
from src.utils.extract_skills import extract_skills_from_superskill_db
import os

class TestExtractSkills(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '../database/metadata_superSkill.json')

    def test_extract_skills_returns_list(self):
        skills = extract_skills_from_superskill_db(self.db_path)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)

    def test_skill_format(self):
        skills = extract_skills_from_superskill_db(self.db_path)
        for skill in skills:
            self.assertIsInstance(skill, str)
            self.assertTrue(skill)

if __name__ == "__main__":
    unittest.main()
