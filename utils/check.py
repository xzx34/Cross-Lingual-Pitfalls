import json
from .prompt import check_question_multiple,extract_check_question,check_question_format,check_question_semantic, check_multiple_choice
from .tools import get_response, clear_json

def check_multiple(mode='reasoning', model='gpt-4o', question=None,max_tries=5):
    prompt = check_question_multiple(question=question)
    response = get_response(model=model, prompt=prompt,temperature=0.0001)
    extracted_prompt=extract_check_question(response)
    while max_tries > 0:
        response = clear_json(get_response(model=model, prompt=extracted_prompt, temperature=0.0001))
        try:
            response = json.loads(response)
            break
        except json.JSONDecodeError:
            max_tries -= 1
            print(f"Failed to extract ideas. Retrying... {max_tries} tries left.")
            continue
    
    
    if max_tries==0 or response['check_result']=='No':
        return False
        
    return True

def check_format(mode='reasoning', model='gpt-4o', question=None,max_tries=5):
    prompt = check_question_format(question=question)
    response = get_response(model=model, prompt=prompt,temperature=0.0001)
    extracted_prompt=extract_check_question(response)
    
    while max_tries > 0:
        response = clear_json(get_response(model=model, prompt=extracted_prompt, temperature=0.0001))
        try:
            response = json.loads(response)
            break
        except json.JSONDecodeError:
            max_tries -= 1
            print(f"Failed to extract ideas. Retrying... {max_tries} tries left.")
            continue
    
    
    if max_tries==0 or response['check_result']=='No':
        return False
        
    return True


def check_semantic(mode='dk', model='gpt-4o', question=None, ori_question=None, ground_truth=None, choices=[], max_tries=5):
    prompt = check_question_semantic(question=question,ori_question=ori_question,ground_truth=ground_truth)
    response = get_response(model='gpt-4o', prompt=prompt,temperature=0.0001)
    extracted_prompt=extract_check_question(response)
    while max_tries > 0:
        response = clear_json(get_response(model='gpt-4o', prompt=extracted_prompt, temperature=0.0001))
        try:
            response = json.loads(response)
            break
        except json.JSONDecodeError:
            max_tries -= 1
            print(f"Failed to extract ideas. Retrying... {max_tries} tries left.")
            continue
    
    if max_tries==0 or response['check_result']=='No':
        return False
    
    return True

