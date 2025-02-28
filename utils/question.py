from .prompt import get_distraction
from .tools import get_response

def generate_question(model='gpt-4o', question=None, wrong_option=None):
    distraction_prompt = get_distraction(question=question, wrong_answer=wrong_option)
    distraction_origin = get_response(model=model, prompt=distraction_prompt, temperature=0.7)
    
    prefix = "Generated Distraction: "
    # extract the content after the prefix
    distraction = distraction_origin[distraction_origin.find(prefix) + len(prefix):]
    if distraction == '':
        return None
    return distraction
