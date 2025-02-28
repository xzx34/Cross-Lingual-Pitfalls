import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .prompt import extract_answer_dk,answer_question_withoutcot
from .tools import get_response, clear_json

def simulate(language='English',question=None, model_list=[], choices=[], ground_truth=None, max_tries=5):
    question_prompt = {
        'Chinese': '请完成以下单选题，并严格从给定的选项中选择一个最符合题意的答案：',
        'English': 'Please complete the following multiple-choice question and select the one option that best fits the given context. Strictly choose from the provided options without adding explanations or modifying the choices: ',
        'French': 'Veuillez répondre à la question à choix unique suivante et sélectionner l’option qui correspond le mieux au contexte donné. Veuillez strictement choisir parmi les options fournies, sans ajouter d’explications ni modifier les choix :',
        'Spanish': 'Por favor, completa la siguiente pregunta de opción múltiple y selecciona la opción que mejor se ajuste al contexto dado. Elige estrictamente entre las opciones proporcionadas sin añadir explicaciones ni modificar las opciones:',
        'Ukrainian':'Будь ласка, завершіть наступне питання з вибором відповіді та виберіть один варіант, який найкраще відповідає даному контексту. Строго обирайте з наданих варіантів без додавання пояснень чи зміни варіантів:',
        'Arabic':'يرجى إكمال سؤال الاختيار من متعدد التالي واختيار الخيار الوحيد الذي يناسب السياق المعطى بشكل أفضل. اختر بدقة من الخيارات المقدمة دون إضافة تفسيرات أو تعديل الخيارات:',
        'Japanese':'次の選択式質問を完成させ、与えられた文脈に最も適した選択肢を1つ選んでください。説明を追加したり、選択肢を変更したりせずに、提供された選択肢から厳密に選んでください:',
        'Korean':'다음 객관식 질문을 완성하고 주어진 상황에 가장 적합한 옵션 하나를 선택하세요. 설명을 추가하거나 선택지를 수정하지 말고 제공된 옵션에서만 엄격히 선택하세요:',
        'German':'Bitte vervollständigen Sie die folgende Multiple-Choice-Frage und wählen Sie die Option aus, die am besten zum gegebenen Kontext passt. Wählen Sie strikt aus den vorgegebenen Optionen, ohne Erklärungen hinzuzufügen oder die Auswahlmöglichkeiten zu ändern:',
        'Italian':f"""Si prega di completare la seguente domanda a scelta multipla e selezionare l'opzione che meglio si adatta al contesto fornito. Scegli esclusivamente tra le opzioni fornite, senza aggiungere spiegazioni o modificare le scelte:""",
        'Portuguese':'Por favor, complete a seguinte pergunta de múltipla escolha e selecione a opção que melhor se adapta ao contexto fornecido. Escolha estritamente entre as opções fornecidas, sem adicionar explicações ou modificar as alternativas:',
        'Bengali':'দয়া করে নিম্নলিখিত বহু নির্বাচনী প্রশ্নটি সম্পূর্ণ করুন এবং প্রদত্ত প্রসঙ্গের সাথে সবচেয়ে ভাল মানানসই একটি বিকল্প নির্বাচন করুন। ব্যাখ্যা যোগ করা বা বিকল্পগুলি পরিবর্তন করা ছাড়াই কেবল সরবরাহকৃত বিকল্পগুলির মধ্য থেকে কঠোরভাবে নির্বাচন করুন।:',
        'Hindi':'कृपया निम्नलिखित बहुविकल्पीय प्रश्न को पूरा करें और दिए गए संदर्भ के अनुसार सबसे उपयुक्त विकल्प का चयन करें। केवल प्रदान किए गए विकल्पों में से ही चयन करें, बिना किसी व्याख्या जोड़े या विकल्पों में बदलाव किए।:',
        'Hebrew':'אנא השלם את שאלת הבחירה המרובה הבאה ובחר את האפשרות שהכי מתאימה להקשר הנתון. בחר אך ורק מתוך האפשרויות שסופקו, מבלי להוסיף הסברים או לשנות את האפשרויות:',
        'Amharic':'እባኮትን የተከታታይውን በርካታ ምርጫ ጥያቄ ሙሉ አድርጉ እና ለተሰጠው ሁኔታ በጣም የሚስማማውን አንድ አማራጭ ይምረጡ። ማብራሪያ ሳታከሉ ወይም አማራጮቹን ሳትለዋወጡ በተሰጡት አማራጮች ብቻ ይምረጡ።:',
        'Yoruba':'Jọwọ parí ìbéèrè ìyanjú-yàn lábẹ́ yìí kí o sì yan aṣayan kan tó bá àkójọ yìí mu jù. Yàn láti inú àwọn àṣàyàn tó wà nìkan, láìfikún àlàyé tàbí yí àwọn àṣàyàn padà:',
        'Swahili':'Tafadhali kamilisha swali lifuatalo la chaguo nyingi na uchague jibu moja linalofaa zaidi kwa muktadha uliotolewa. Chagua tu kutoka kwa chaguo zilizotolewa bila kuongeza maelezo au kubadilisha chaguo hizo:',
        'Zulu':'Sicela uqede umbuzo olandelayo wokukhetha okuningi bese ukhetha inketho eyodwa ehambisana kakhulu nomongo onikeziwe. Khetha ngokuqinile ezinkethweni ezinikeziwe ngaphandle kokungeza izincazelo noma ukuguqula izinketho:'
    }
    prompt = question_prompt[language]+answer_question_withoutcot(question=question, choices=choices)
    responses = []

    def get_answer_dk(model='gpt-4o'):
        tries = max_tries
        response = get_response(model=model, prompt=prompt, temperature=0.0001)
        extract_prompt = extract_answer_dk(question=question, answer=response, choices=choices)
        answer = clear_json(get_response(model='gpt-4o-mini', prompt=extract_prompt, temperature=0.0001))
        if answer==None:
            print(f"Failed to extract answer.")
            tries -= 1
            return 
        try:
            answer = json.loads(answer)['final_answer']
            if answer in choices:
                print(f"{model}: {answer}")
                return answer
            else:
                tries -= 1
                print(f"Out of choices")
        except json.JSONDecodeError:
            print(f"Failed to extract answer.")
            return 1  # Return None if all tries are exhausted

    with ThreadPoolExecutor() as executor:
        future_answers = [executor.submit(get_answer_dk, model) for model in model_list]
        for future in as_completed(future_answers):
            result = future.result()
            if result:
                responses.append(result)
    
    correct_number = 0
    for value in responses:
        if value == ground_truth:
            correct_number += 1
    if len(responses) == 0:
        correct_rate = 0
    else : 
        correct_rate = correct_number / len(responses)
    return correct_rate