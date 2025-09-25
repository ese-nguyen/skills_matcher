from src.utils.extract_skills import extract_skills_from_superskill_db
from src.core.matcher import match_skills

def main():
    # Extract standardized skills and save to file
    skills = extract_skills_from_superskill_db("./data/database/metadata_superSkill.json")
    with open("./data/skills.txt", "w", encoding="utf-8") as f:
        for skill in skills:
            f.write(skill + "\n")

    # Example: match a sample list of raw skills
    raw_skills = [
        "AI", "Machine learning", "TSNE", "data analysis", "privacy law", "unknown skill"
    ]
    results = match_skills(raw_skills)
    print("Skill Matching Results:")
    for item in results:
        print(item)

    # Optionally, save results to file
    with open("./data/matched_skills.json", "w", encoding="utf-8") as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
