import json
from .prompt import English2Chinese,extract_transquestion,English2French,English2all,English2Spanish,English2Ukrainian,English2Arabic,English2Japanese,English2Korean,English2German,English2Italian,English2Portuguese,English2Bengali,English2Hindi,English2Hebrew,English2Amharic,English2Yoruba,English2Swahili,English2Zulu
from .tools import get_response, clear_json

def translate_question(model='gpt-4o-mini',target='Chinese',question=None,choices=[],ground_truth=None,max_tries=5):
    if target=='Chinese':
        prompt = English2Chinese(question=question, choices=choices,ground_truth=ground_truth)
    if target=='French':
        prompt = English2French(question=question, choices=choices,ground_truth=ground_truth)
    if target =='Spanish':
        prompt= English2Spanish(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Ukrainian':
        prompt= English2Ukrainian(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Arabic':
        prompt= English2Arabic(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Japanese':
        prompt= English2Japanese(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Korean':
        prompt= English2Korean(question=question, choices=choices,ground_truth=ground_truth)
    if target=='German':
        prompt= English2German(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Italian':
        prompt= English2Italian(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Portuguese':
        prompt= English2Portuguese(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Bengali':
        prompt= English2Bengali(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Hindi':
        prompt= English2Hindi(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Hebrew':
        prompt= English2Hebrew(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Amharic':
        prompt= English2Amharic(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Yoruba':
        prompt= English2Yoruba(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Swahili':
        prompt= English2Swahili(question=question, choices=choices,ground_truth=ground_truth)
    if target=='Zulu':
        prompt= English2Zulu(question=question, choices=choices,ground_truth=ground_truth)
    response = get_response(model=model, prompt=prompt, temperature=0.7)
    extracted_prompt=extract_transquestion(response)
    while max_tries > 0:
        response = clear_json(get_response(model='gpt-4o-mini', prompt=extracted_prompt, temperature=0.0001))
        try:
            response = json.loads(response)
            return response
        except json.JSONDecodeError:
            print("json error")
            return None

def translate_text(model='gpt-4o-mini',ori='English',target='Chinese',text=None):
    if text == '':
        return ''

    prompt = English2all(target=target,text=text)
    response = get_response(model=model, prompt=prompt, temperature=0.01)
    if response == '':
        return None
    return response
