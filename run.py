from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import numpy as np
import argparse
import json
from utils.answers import simulate
from utils.question import generate_question
from utils.tools import logger as utils_logger
from utils.translate import translate_question, translate_text
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# Configure logging
logger = utils_logger
count={}
def add_count(question=None):
    if question in count:
        count[question]+=1
    else:
        count[question]=1
def evaluate_function(rate_ori=1, rate_trans=1, p=2, q=2, r=3, alpha=20):
    reward = np.log(1 + (rate_ori ** p) / (rate_trans ** q + 0.001))
    penalty = alpha * ((1 - rate_ori) ** r)
    result = reward - penalty
    return result

def process_entry(entry, model_list, args):
    """
    Process a single entry (question) and return new generated questions.
    """
    result = []
    try:
        oriquestion, prequestion, sufquestion, choices, answer, source, transori, transpre, transsuf, transchoices, transanswer = (
            entry.get(key) for key in [
                "oriquestion", "prequestion", "sufquestion", "choices", "answer", "source", 
                "transori", "transpre", "transsuf", "transchoices", "transanswer"
            ]
        )
        wrong_options = [choice for choice in choices if choice !=answer]
        for wrong_option in wrong_options:  
            try:
                new_question =entry.copy()
                distraction = generate_question(
                    model='gpt-4o-mini',
                    question=prequestion+oriquestion+sufquestion,
                    wrong_option=wrong_option,
                )
                if not distraction:
                    logger.warning("Failed to generate distraction.")
                    continue  
                
                trans_distraction=translate_text(model='gpt-4o',ori='English',target=args.language, text=distraction)
                if not distraction:
                    logger.warning("Failed to translate distraction.")
                    continue  
                if len(distraction) %2==1:
                    new_question['prequestion'] = distraction+prequestion
                    new_question['transpre'] = trans_distraction+transpre
                else:
                    new_question['sufquestion'] = sufquestion+distraction
                    new_question['transsuf'] = transsuf+trans_distraction
                
                shuffled_choices = choices[:]
                new_question['choices']=shuffled_choices
                shuffled_choices = transchoices[:]
                new_question['transchoices']=shuffled_choices
                new_question['question'] = new_question['prequestion']+new_question['oriquestion']+new_question['sufquestion']
                new_question['transquestion'] = new_question['transpre']+new_question['transori']+new_question['transsuf']
                try:
                    rate_ori = simulate(
                        language='English',
                        question=new_question['question'],
                        model_list=model_list,
                        choices=new_question['choices'],
                        ground_truth=answer,
                    )
                    logger.info(f"Original simulation rate: {rate_ori}")
                except Exception as e:
                    logger.error(f"Error in simulate (rate_ori): {e}")
                    continue
                if rate_ori != 1:
                    continue 
                try:
                    rate_trans = simulate(
                        language=args.language,
                        question=new_question['transquestion'],
                        model_list=model_list,
                        choices=new_question['transchoices'],
                        ground_truth=transanswer,
                    )
                    logger.info(f"Translated simulation rate: {rate_trans}")
                except Exception as e:
                    logger.error(f"Error in simulate (rate_trans): {e}")
                    continue
                try:
                    value = evaluate_function(rate_ori=rate_ori, rate_trans=rate_trans)
                    logger.info(f"Evaluated value: {value}")
                except Exception as e:
                    logger.error(f"Error in evaluate_function: {e}")
                    continue

                new_question['value'] = value
                new_question['rate_ori'] = rate_ori
                new_question['rate_trans'] = rate_trans
                result.append(new_question)

            except Exception as e:
                logger.error(f"Error processing idea: {e}")
                continue

    except Exception as e:
        logger.error(f"Error processing entry: {e}")
    return result

def work(batch, model_list, args, now_time, max_times=3):
    if now_time >= max_times or batch==[]:
        logger.info(f"Maximum recursion depth reached: now_time={now_time}, max_times={max_times}")
        return
    logger.info("\n\n=================Processing a new batch====================")
    logger.info(f"now_time={now_time}, max_times={max_times}")

    new_questions = []
    output_file = args.output_file
    
    with ThreadPoolExecutor(max_workers=args.max_queue) as executor:
        future_to_entry = {executor.submit(process_entry, entry, model_list, args): entry for entry in batch}
        for future in as_completed(future_to_entry):
            try:
                result = future.result()
                new_questions.extend(result)
            except Exception as e:
                logger.error(f"Error in concurrent processing: {e}")

    new_questions.sort(key=lambda x: x['value'], reverse=True)

    good_questions = []
    
    for question in new_questions[:]: 
        logger.info(f"\nEvaluating question: {question}")
        if question['rate_ori'] == 1 and question['rate_trans'] <= 0.4:
            max_times = 6
            logger.info("Good question identified!")
            good_questions.append(question)
            if question['rate_trans'] <= 0.2:
                add_count(question['oriquestion'])
            if question['rate_trans']==0:
                new_questions.remove(question)
                
        
    for question in new_questions: 
        if question['rate_ori'] !=1:
            new_questions.remove(question)
        elif count.get(question['oriquestion']) and count[question['oriquestion']] >= args.max_good:
            new_questions.remove(question)

    if good_questions:
        try:
            existing_questions = []
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_questions = json.load(f)

            existing_questions.extend(good_questions)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(existing_questions, f, ensure_ascii=False, indent=4)
                logger.info(f"\nAppended {len(good_questions)} new good questions. Total now: {len(existing_questions)}.")
        except Exception as e:
            logger.error(f"Error appending good questions: {e}")
    
    next_batch = new_questions[:args.max_queue]
    return work(batch=next_batch, model_list=model_list, args=args, now_time=now_time + 1, max_times=max_times)

def main():
    parser = argparse.ArgumentParser(description="Single File Question Processing Script")
    parser.add_argument('--input-file', type=str, default='data/source/mmlu.json', help='Path to the input JSON file containing questions.')
    parser.add_argument('--output-file', type=str, default='data/mmlu_Chinese.json', help='Path to the output JSON file containing weaknesses.')
    parser.add_argument('--language', type=str, default='Chinese', help='')
    parser.add_argument('--max-good', type=int, default=3, help='Maximum number of good questions to find per entry.')
    parser.add_argument('--max-queue', type=int, default=12, help='Width of the queue for processing.')
    parser.add_argument('--batch-size', type=int, default=4, help='')
    parser.add_argument('--models', type=str, nargs='+', default=['gpt-4o', 'llama-3.1-8B', 'qwen-2.5-72B', 'gpt-4o-mini', 'gemma-2-27B'], help='Simulation models.')

    args = parser.parse_args()
    model_list = args.models
    

    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    batch_size = args.batch_size
    impossible_num = 0
    batch = []

    for i in range(len(data)):
        logger.info(f"Impossible_num: {impossible_num}/{i}")
        entry = data[i]
        entry['oriquestion'] = entry['question']
        
        rate_ori = simulate(
            language='English',
            question=entry['question'],
            model_list=model_list,
            choices=entry['choices'],
            ground_truth=entry['answer'],
        )
        
        if rate_ori != 1.0:
            impossible_num += 1
            continue  # Skip this entry since it's not suitable

        # If rate_ori is 1.0, attempt to translate
        trans_entry = translate_question(
            model='gpt-4o',
            target=args.language,
            question=entry['question'],
            choices=entry['choices'],
            ground_truth=entry['answer']
        )

        if trans_entry is None:
            continue  # Skip this entry if translation fails
        print(trans_entry['choices'])
        # Add the translated information to the entry
        entry['transori'] = trans_entry['text']
        entry['transchoices'] = trans_entry['choices']
        entry['transanswer'] = trans_entry['answer']
        entry['prequestion'] = ''
        entry['sufquestion'] = ''
        entry['transpre'] = ''
        entry['transsuf'] = ''
        
        batch.append(entry)

        # If the batch has reached the desired size, process it
        if len(batch) == batch_size:
            work(batch=batch, model_list=model_list, args=args, now_time=0, max_times=4)
            logger.info(f"Batch processed with {batch_size} valid entries.")
            batch = []  # Reset batch for the next set of entries

    # If there are leftover entries in the batch that didn't form a full batch_size group, process them
    if batch:
        work(batch=batch, model_list=model_list, args=args, now_time=0, max_times=4)
        logger.info(f"Final batch processed with {len(batch)} valid entries.")

if __name__ == "__main__":
    main()
