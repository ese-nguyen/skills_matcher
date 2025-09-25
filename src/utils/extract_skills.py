import json
from typing import List



from typing import List, Dict

def extract_skills_from_superskill_db(json_path: str) -> List[Dict]:
    """
    Extract all skill names and elId from the superskill database JSON file.
    Args:
        json_path (str): Path to the superskill database JSON file.
    Returns:
        List[Dict]: List of dicts with 'elId' and 'value'.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    skills = []
    for entry in data:
        if entry.get('key') == 'skills' and 'val' in entry:
            for skill in entry['val'].values():
                skills.append({
                    'elId': skill.get('elId'),
                    'value': skill.get('value')
                })
    return skills
