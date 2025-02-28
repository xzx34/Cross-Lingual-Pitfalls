import json
from .prompt import get_ideas, extract_ideas
from .tools import get_response, clear_json

def generate_ideas(model='gpt-4o',question=None, answer=None, choices=[],max_tries=5):
    wrong_choices = [choice for choice in choices if choice != answer]
    prompt = get_ideas(question=question, choices=wrong_choices)
    original_ideas = get_response(model=model, prompt=prompt, temperature=0.7)
    extracted_prompt = extract_ideas(prompt=original_ideas, number=len(wrong_choices))
    while max_tries > 0:
        ideas = clear_json(get_response(model='gpt-4o-mini', prompt=extracted_prompt, temperature=0.0001))
        try:
            ideas = json.loads(ideas)
            return ideas
        except json.JSONDecodeError:
            max_tries -= 1
            print(f"Failed to extract ideas. Retrying... {max_tries} tries left.")
            continue

