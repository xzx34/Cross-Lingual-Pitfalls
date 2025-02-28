import os
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from utils.answers import simulate
from utils.tools import logger as utils_logger

logger = utils_logger

def main():
    parser = argparse.ArgumentParser(description="Process language-specific questions for various models.")
    parser.add_argument("--lang", default='Chinese', help="The language to process (e.g., 'French').")
    parser.add_argument("--input_file", default='data/Chinese.json', help="The input JSON file.")
    parser.add_argument("--output_file", default='data/Chinese_results.json', help="The output JSON file.")
    args = parser.parse_args()
    lang = args.lang
    input_file = args.input_file
    output_file = args.output_file

    models = ['qwen-2.5-7B', 'llama-3.1-8B', 'gemma-2-9B', 'gemma-2-27B','llama-3.1-70B', 'qwen-2.5-72B', 'gpt-4o-mini', 'gpt-4o', 'yi-lightning','o1-mini','claude-3.5-sonnet']
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                logger.error("The input JSON file should be a list.")
                return
    except Exception as e:
        logger.error(f"Failed to load the input file: {e}")
        return
    
    filtered_data = [entry for entry in data if entry['rate_trans'] <= 0.2]

    def process_model(model, entry, results):
        model_list = [model]
        eng_correct = simulate(
            language='English',
            question=entry['question'],
            model_list=model_list,
            choices=entry['choices'],
            ground_truth=entry['answer'],
        )
        results['English'][model] += eng_correct

        chi_correct = simulate(
            language=lang if lang != '4o' else 'Chinese',
            question=entry.get('transquestion', ''),
            model_list=model_list,
            choices=entry.get('transchoices', []),
            ground_truth=entry.get('transanswer', ''),
        )
        results[lang][model] += chi_correct

    def process_data():
        results = {
            'English': {model: 0 for model in models},
            lang: {model: 0 for model in models},
            'Total Questions': 0
        }
        
        with ThreadPoolExecutor() as executor:
            future_tasks = []
            for entry in filtered_data:
                # Increment Total Questions only once per question
                results['Total Questions'] += 1
                for model in models:
                    future = executor.submit(process_model, model, entry, results)
                    future_tasks.append(future)
            for future in future_tasks:
                future.result()

        return results

    current_results = process_data()

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f_out:
                existing_results = json.load(f_out)
                if not all(key in existing_results for key in ['English', lang, 'Total Questions']):
                    logger.warning("Existing JSON structure is incomplete. Reinitializing.")
                    existing_results = {
                        'English': {model: 0 for model in models},
                        lang: {model: 0 for model in models},
                        'Total Questions': 0
                    }
        except Exception as e:
            logger.error(f"Failed to load existing results: {e}")
            existing_results = {
                'English': {model: 0 for model in models},
                lang: {model: 0 for model in models},
                'Total Questions': 0
            }
    else:
        existing_results = {
            'English': {model: 0 for model in models},
            lang: {model: 0 for model in models},
            'Total Questions': 0
        }

    for language in ['English', lang]:
        for model in models:
            if model not in existing_results[language]:
                existing_results[language][model] = current_results[language][model]
            else:
                existing_results[language][model] += current_results[language][model]

    print(f"Total Questions = {existing_results['Total Questions']}")
    print("English")
    print(existing_results['English'])
    print(lang)
    print(existing_results[lang])

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            json.dump(existing_results, f_out, ensure_ascii=False, indent=4)
        logger.info(f"Results have been successfully saved to {output_file}")
    except Exception as e:
        logger.error(f"Failed to save results to {output_file}: {e}")

if __name__ == "__main__":
    main()
