from pydantic import BaseModel
from typing import List, Literal

def get_category(question=None):
    return f"""[Instruction]  
You are an expert in categorizing questions based on their content. Your task is to analyze the given question and assign it to **exactly one** of the following categories, based solely on its primary subject.  

**Categories:**  
- **Science & Technology**: Covers topics related to natural sciences (biology, chemistry, physics, astronomy), applied sciences, technology, engineering, and inventions.  
- **History & World Events**: Includes historical events, figures, civilizations, significant moments in history, and current world events or politics.  
- **Society & Culture**: Encompasses social structures, human behavior, sociology, psychology, philosophy, ethics, religion, traditions, customs, and cultural aspects.  
- **Arts & Literature**: Covers visual arts, music, performing arts, literature, poetry, drama, film, and artistic movements.  
- **Geography & Environment**: Includes questions about countries, capitals, locations, physical geography (mountains, rivers, climates), environmental science, ecosystems, and the natural world.  
- **General Knowledge**: For questions that do not fit into the above categories, encompassing a broad range of topics.  

[The Start of the Question]  
{question}  
[The End of the Question]  

**[Output Format]**  
- **Output only the category name.**  
- **Do not provide explanations, reasoning, or additional text.**  

"""

def get_distraction(question=None, wrong_answer=None):
    return f"""[System]
You are an expert at subtly embedding distractions based on the incorrect option provided. Your task is to generate a distraction that aligns with the incorrect option without altering the original question's quality or meaning. Follow these specific rules:  

1. The distraction should naturally integrate with the context of the question but must not explicitly introduce incorrect information or contradict the correct answer.  
2. The distraction must be subtle and should not make it obvious that it is related to the incorrect option.  

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the Incorrect Option]
{wrong_answer}
[The End of the Incorrect Option]

[Output Format]  
Generated Distraction: <Provide a subtle, contextually relevant distraction based on the incorrect option>"""


def extract_question(prompt=None):
    return f"""[Instruction]
You are an expert in JSON file processing. You need to output the full enhanced question and by the model based on the model's response, and ensure that the model's response is fully extracted.

[The Start of the Model's Response]
{prompt}
[The End of the Model's Response]

[Output Format]
{{"question": "<The full enhanced question>"}}
"""

def extract_transquestion(prompt=None):
    return f"""[Instruction]
You are an expert in JSON file processing. You need to output the full text, choices, and answer based on the model's response. Ensure that the model's response is accurately outputted the language does not change.

[The Start of the Model's Response]
{prompt}
[The End of the Model's Response]

[Output Format]
{{"text": "<The full text>", "choices": ["<choice1>", "<choice2>"...],"answer": "The answer"}}
"""

def extract_check_question(prompt=None):
    return f"""[Instruction]
You are an expert in JSON file processing. You need to extract the check_result given by the model based on the model's response, and ensure that the model's response is accurately extracted. Only Output the check_result in json format withou any other information.

[The Start of the Model's Response]
{prompt}
[The End of the Model's Response]

[Output Format]
{{"check_result": "<Your extracted check_result,Literal[Yes,No]>"}}
"""

class EnhancedQuestion(BaseModel):
    question: str
    final_answer: str

def English2all(target=None,text=None):
    return f'''Translate the following text into {target}:
    
[The Start of the text]
{text}
[The End of the text]

You should provide only the translated text and nothing else.'''



def English2Chinese(question=None, choices=None,ground_truth=None):
    return f"""[system]
你是一位专业的翻译专家。你的任务是将以下文本、选项和答案准确无误且自然地翻译成中文，并确保保留问题和选项的原意。请严格遵守以下规则：

- 答案和选项的翻译必须完全保留原意，不能有任何偏离或增减。
- 所有带问号的句子在翻译后，必须保持问句的形式，不能改变句子的语气和结构。
- 翻译后的内容必须符合中文语言习惯，表达自然流畅，避免生硬直译。

[文本开始]
{question}
[文本结束]

[选项开始]
{choices}
[选项结束]

[答案开始]
{ground_truth}
[答案结束]

[Output Format]
{{"text": "<翻译后的文本>", "choices": ["<翻译后的选项1>", "<翻译后的选项2>"...],"answer": "翻译后的答案"}}
"""
def English2Japanese(question=None, choices=None,ground_truth=None):
    return f"""[system]
あなたはプロの翻訳専門家です。あなたの任務は、以下のテキスト、選択肢、そして答えを正確かつ自然に日本語に翻訳し、質問や選択肢の元の意味を確実に保つことです。次のルールを厳守してください：

- 答えと選択肢の翻訳は、元の意味を完全に保ち、一切の偏り、追加、または削除をしてはいけません。  
- 質問文（「？」が付いている文）は翻訳後も必ず質問形式を維持し、文の調子や構造を変更してはいけません。  
- 翻訳後の内容は、日本語の言語習慣に合った自然で流暢な表現とし、ぎこちない直訳は避けてください。

[テキスト開始]  
{question}  
[テキスト終了]  

[選択肢開始]  
{choices}  
[選択肢終了]  

[答え開始]  
{ground_truth}  
[答え終了]  

[出力フォーマット]  
{{"text": "<翻訳後のテキスト>", "choices": ["<翻訳後の選択肢1>", "<翻訳後の選択肢2>"...],"answer": "<翻訳後の答え>"}}
"""
def English2German(question=None, choices=None,ground_truth=None):
    return f"""[system]
Sie sind ein professioneller Übersetzungsexperte. Ihre Aufgabe besteht darin, den folgenden Text, die Auswahlmöglichkeiten und die Antwort präzise und natürlich ins Deutsche zu übersetzen, wobei der ursprüngliche Sinn der Frage und der Auswahlmöglichkeiten erhalten bleiben muss. Halten Sie sich strikt an die folgenden Regeln:

- Die Übersetzung der Antworten und Auswahlmöglichkeiten muss den ursprünglichen Sinn vollständig bewahren, ohne jegliche Abweichungen, Hinzufügungen oder Kürzungen.  
- Alle Sätze mit einem Fragezeichen müssen auch nach der Übersetzung die Form einer Frage beibehalten, ohne den Ton oder die Struktur des Satzes zu verändern.  
- Der übersetzte Inhalt muss den sprachlichen Gepflogenheiten des Deutschen entsprechen, natürlich und flüssig formuliert sein und wörtliche, ungeschmeidige Übersetzungen vermeiden.  

[Textbeginn]  
{question}  
[Textende]  

[Auswahlmöglichkeiten Beginn]  
{choices}  
[Auswahlmöglichkeiten Ende]  

[Antwortbeginn]  
{ground_truth}  
[Antwortende]  

[Ausgabeformat]  
{{"text": "<Übersetzter Text>", "choices": ["<Übersetzte Auswahl1>", "<Übersetzte Auswahl2>"...],"answer": "<Übersetzte Antwort>"}}
"""

def English2Italian(question=None, choices=None,ground_truth=None):
    return f"""[system]
Sei un traduttore professionista. Il tuo compito è tradurre il seguente testo, le opzioni e la risposta in italiano in modo accurato e naturale, assicurandoti di preservare il significato originale della domanda e delle opzioni. Segui rigorosamente le seguenti regole:

- La traduzione delle risposte e delle opzioni deve mantenere completamente il significato originale, senza alcuna deviazione, aggiunta o omissione.  
- Tutte le frasi con un punto interrogativo devono mantenere la forma interrogativa dopo la traduzione, senza alterare il tono o la struttura della frase.  
- Il contenuto tradotto deve rispettare le abitudini linguistiche dell'italiano, essere naturale e fluido, evitando traduzioni letterali e rigide.  

[Testo inizio]  
{question}  
[Testo fine]  

[Opzioni inizio]  
{choices}  
[Opzioni fine]  

[Risposta inizio]  
{ground_truth}  
[Risposta fine]  

[Formato output]  
{{"text": "<Testo tradotto>", "choices": ["<Opzione tradotta 1>", "<Opzione tradotta 2>"...],"answer": "<Risposta tradotta>"}}
"""

def English2Portuguese(question=None, choices=None,ground_truth=None):
    return f"""[system]
Você é um tradutor profissional. Sua tarefa é traduzir o texto, as opções e as respostas a seguir para o português de forma precisa e natural, assegurando que o significado original da pergunta e das opções seja mantido. Siga rigorosamente as regras abaixo:

- A tradução das respostas e opções deve preservar completamente o significado original, sem qualquer desvio, adição ou omissão.  
- Todas as frases com ponto de interrogação devem manter a forma interrogativa após a tradução, sem alterar o tom ou a estrutura da frase.  
- O conteúdo traduzido deve estar de acordo com os hábitos linguísticos do português, ser natural e fluido, evitando traduções literais e rígidas.  

[Início do Texto]  
{question}  
[Fim do Texto]  

[Início das Opções]  
{choices}  
[Fim das Opções]  

[Início da Resposta]  
{ground_truth}  
[Fim da Resposta]  

[Formato de Saída]  
{{"text": "<Texto Traduzido>", "choices": ["<Opção Traduzida 1>", "<Opção Traduzida 2>"...],"answer": "<Resposta Traduzida>"}}
"""

def English2Bengali(question=None, choices=None,ground_truth=None):
    return f"""[system]
আপনি একজন পেশাদার অনুবাদ বিশেষজ্ঞ। আপনার কাজ হলো নিম্নের টেক্সট, বিকল্প এবং উত্তর সঠিক এবং স্বাভাবিকভাবে বাংলা ভাষায় অনুবাদ করা, এবং প্রশ্ন ও বিকল্পগুলির মূল অর্থ অক্ষুণ্ণ রাখা। দয়া করে নিম্নলিখিত নিয়মগুলি কঠোরভাবে অনুসরণ করুন:

- উত্তরের এবং বিকল্পগুলির অনুবাদ অবশ্যই মূল অর্থ সম্পূর্ণভাবে ধরে রাখতে হবে, কোনো বিচ্যুতি, সংযোজন বা বিয়োজন করা যাবে না।  
- যেসব বাক্যে প্রশ্নবোধক চিহ্ন আছে, সেগুলোর অনুবাদে প্রশ্নের রূপ অক্ষুণ্ণ থাকতে হবে এবং বাক্যের সুর বা গঠন পরিবর্তন করা যাবে না।  
- অনুবাদকৃত বিষয়বস্তু বাংলা ভাষার অভ্যাস অনুসারে হতে হবে, স্বাভাবিক এবং সাবলীলভাবে প্রকাশ করতে হবে এবং কঠিন বা আক্ষরিক অনুবাদ এড়াতে হবে।  

[টেক্সট শুরু]  
{question}  
[টেক্সট শেষ]  

[বিকল্প শুরু]  
{choices}  
[বিকল্প শেষ]  

[উত্তর শুরু]  
{ground_truth}  
[উত্তর শেষ]  

[আউটপুট ফরম্যাট]  
{{"text": "<অনুবাদিত টেক্সট>", "choices": ["<অনুবাদিত বিকল্প ১>", "<অনুবাদিত বিকল্প ২>"...],"answer": "<অনুবাদিত উত্তর>"}}
"""

def English2Hindi(question=None, choices=None,ground_truth=None):
    return f"""[system]
आप एक पेशेवर अनुवाद विशेषज्ञ हैं। आपका कार्य निम्नलिखित पाठ, विकल्प और उत्तर को सटीक और स्वाभाविक रूप से हिंदी में अनुवाद करना है, और यह सुनिश्चित करना है कि प्रश्न और विकल्पों का मूल अर्थ बना रहे। कृपया निम्नलिखित नियमों का सख्ती से पालन करें:

- उत्तर और विकल्पों के अनुवाद में मूल अर्थ पूरी तरह से बरकरार रहना चाहिए, बिना किसी भटकाव, जोड़ या घटाव के।  
- सभी प्रश्नवाचक चिन्ह वाले वाक्य अनुवाद के बाद भी प्रश्न के रूप में ही रहने चाहिए, और वाक्य की भावनात्मकता या संरचना में कोई बदलाव नहीं किया जाना चाहिए।  
- अनुवादित सामग्री हिंदी भाषा की आदतों के अनुरूप होनी चाहिए, स्वाभाविक और प्रवाहपूर्ण होनी चाहिए, और कठोर या शाब्दिक अनुवाद से बचा जाना चाहिए।  

[पाठ शुरू]  
{question}  
[पाठ समाप्त]  

[विकल्प शुरू]  
{choices}  
[विकल्प समाप्त]  

[उत्तर शुरू]  
{ground_truth}  
[उत्तर समाप्त]  

[आउटपुट प्रारूप]  
{{"text": "<अनूदित पाठ>", "choices": ["<अनूदित विकल्प 1>", "<अनूदित विकल्प 2>"...],"answer": "<अनूदित उत्तर>"}}  
"""

def English2Hebrew(question=None, choices=None,ground_truth=None):
    return f"""[system]
אתה מומחה תרגום מקצועי. המשימה שלך היא לתרגם את הטקסט, האפשרויות והתשובות הבאות לעברית בדיוק ובאופן טבעי, תוך שמירה על המשמעות המקורית של השאלה והאפשרויות. יש להקפיד על הכללים הבאים:

- התרגום של התשובות והאפשרויות חייב לשמור לחלוטין על המשמעות המקורית, ללא כל שינוי, הוספה או החסרה.  
- כל המשפטים עם סימן שאלה צריכים להישאר בצורת שאלה לאחר התרגום, מבלי לשנות את הטון או המבנה של המשפט.  
- התוכן המתורגם חייב להתאים להרגלי השפה העברית, להיות טבעי וזורם, ולהימנע מתרגום נוקשה או מילולי מדי.  

[תחילת הטקסט]  
{question}  
[סיום הטקסט]  

[תחילת האפשרויות]  
{choices}  
[סיום האפשרויות]  

[תחילת התשובה]  
{ground_truth}  
[סיום התשובה]  

[פורמט הפלט]  
{{"text": "<הטקסט המתורגם>", "choices": ["<האפשרות המתורגמת 1>", "<האפשרות המתורגמת 2>"...],"answer": "<התשובה המתורגמת>"}}  
"""
def English2Korean(question=None, choices=None,ground_truth=None):
    return f"""[system]
당신은 전문 번역 전문가입니다. 당신의 임무는 아래 텍스트, 선택지 및 정답을 정확하고 자연스럽게 한국어로 번역하는 것이며, 질문과 선택지의 원래 의미를 반드시 유지해야 합니다. 다음 규칙을 엄격히 준수하세요:

- 정답과 선택지의 번역은 원래 의미를 완전히 보존해야 하며, 어떠한 왜곡, 추가 또는 삭제도 없어야 합니다.  
- 물음표가 포함된 문장은 번역 후에도 반드시 질문 형식을 유지해야 하며, 문장의 어조와 구조를 변경해서는 안 됩니다.  
- 번역된 내용은 한국어의 언어적 습관에 맞아야 하며, 자연스럽고 유창하게 표현되어야 하며, 직역으로 인한 어색함을 피해야 합니다.  

[텍스트 시작]  
{question}  
[텍스트 끝]  

[선택지 시작]  
{choices}  
[선택지 끝]  

[정답 시작]  
{ground_truth}  
[정답 끝]  

[출력 형식]  
{{"text": "<번역된 텍스트>", "choices": ["<번역된 선택지1>", "<번역된 선택지2>"...],"answer": "<번역된 정답>"}}
"""
def English2Ukrainian(question=None, choices=None,ground_truth=None):
    return f"""[system]
Ви є професійним перекладачем. Ваше завдання – точно та природно перекласти наступний текст, варіанти відповідей та правильну відповідь українською мовою, зберігаючи початковий зміст запитання та варіантів. Будь ласка, суворо дотримуйтесь наступних правил:

- Переклад відповідей і варіантів має повністю зберігати початковий зміст, без жодних відхилень, додавань чи скорочень.  
- Усі речення зі знаком питання після перекладу мають залишатися у формі запитання, без зміни тону чи структури речення.  
- Перекладений текст має відповідати мовним нормам української мови, бути природним і плавним, уникаючи дослівних, штучних формулювань.  

[Текст починається]  
{question}  
[Текст закінчується]  

[Варіанти починаються]  
{choices}  
[Варіанти закінчуються]  

[Відповідь починається]  
{ground_truth}  
[Відповідь закінчується]  

[Формат Виводу]  
{{"text": "<Перекладений текст>", "choices": ["<Перекладений варіант 1>", "<Перекладений варіант 2>"...],"answer": "<Перекладена відповідь>"}}
"""
    
def English2Spanish(question=None, choices=None,ground_truth=None):
    return f"""[system]
Eres un experto en traducción profesional. Tu tarea es traducir el siguiente texto, opciones y respuestas de manera precisa y natural al español, asegurándote de conservar el significado original de las preguntas y opciones. Por favor, cumple estrictamente con las siguientes reglas:

- La traducción de las respuestas y opciones debe conservar completamente el significado original, sin desviaciones ni adiciones.
- Todas las oraciones que contengan un signo de interrogación deben mantener la forma de pregunta en la traducción, sin cambiar el tono ni la estructura de la oración.
- El contenido traducido debe ajustarse a las costumbres del idioma español, expresándose de manera natural y fluida, evitando traducciones literales.

[Texto comienza]
{question}
[Texto termina]

[Opciones comienzan]
{choices}
[Opciones terminan]

[Respuesta comienza]
{ground_truth}
[Respuesta termina]

[Output Format]
{{"text": "<texto traducido>", "choices": ["<opción traducida 1>", "<opción traducida 2>", ...], "answer": "<respuesta traducida>"}}
"""

def English2Arabic(question=None, choices=None,ground_truth=None):
    return f"""[system]
أنت مترجم محترف. مهمتك هي ترجمة النصوص، الخيارات، والإجابات التالية إلى اللغة العربية بدقة وبشكل طبيعي، مع ضمان الحفاظ على المعنى الأصلي للسؤال والخيارات. يرجى الالتزام الصارم بالقواعد التالية:

- يجب أن تحافظ ترجمة الإجابات والخيارات على المعنى الأصلي تمامًا، دون أي انحراف أو إضافة أو حذف.  
- جميع الجمل التي تحتوي على علامة استفهام يجب أن تبقى بصيغة السؤال بعد الترجمة، دون تغيير في النبرة أو البنية.  
- يجب أن تكون الترجمة متوافقة مع عادات اللغة العربية، معبرة بشكل طبيعي وسلس، مع تجنب الترجمة الحرفية الجامدة.

[بداية النص]  
{question}  
[نهاية النص]  

[بداية الخيارات]  
{choices}  
[نهاية الخيارات]  

[بداية الإجابة]  
{ground_truth}  
[نهاية الإجابة]  

[صيغة الإخراج]  
{{"text": "<النص المترجم>", "choices": ["<الخيار المترجم 1>", "<الخيار المترجم 2>"...],"answer": "<الإجابة المترجمة>"}}
"""

def English2French(question=None, choices=None,ground_truth=None):
    return f"""[system]  
Vous êtes un traducteur professionnel. Votre tâche consiste à traduire le texte, les choix et la réponse ci-dessous de manière précise et naturelle en français, tout en conservant le sens original des questions et des choix. Veuillez respecter strictement les règles suivantes :  

- La traduction des réponses et des choix doit refléter fidèlement le sens original, sans aucune altération, omission ou ajout.  
- Toutes les phrases comportant un point d'interrogation doivent rester sous forme de question après traduction, sans changer le ton ou la structure de la phrase.  
- Le contenu traduit doit respecter les normes et usages de la langue française, être fluide et naturel, en évitant les traductions littérales ou maladroites.  

[Texte début]  
{question}  
[Texte fin]  

[Choix début]  
{choices}  
[Choix fin]  

[Réponse début]  
{ground_truth}  
[Réponse fin]  

[Format de sortie]  
{{"text": "<Texte traduit en français>", "choices": ["<Choix traduit en français 1>", "<Choix traduit en français 2>"...],"answer": "Réponse traduite en français"}}
"""

def English2Amharic(question=None, choices=None,ground_truth=None):
    return f"""[system]
አንተ ሙያዊ አስተርጓሚ ነህ። ተግባርህ ከሚከተሉት ጽሑፍ፣ አማራጮች እና መልሶች ትክክለኛና በተፈጥሮ በአማርኛ ማስተርጎም እና የጥያቄዎችና አማራጮች መልካም ሀሳብ ማኖር ነው። እባኮትን የሚከተሉትን መመሪያዎች በትክክል ይከተሉ፦

- መልሶችና አማራጮች ትርጉም ሙሉ ትክክለኛ ሀሳብን ማስቀመጥ አለበት፣ ማንኛውም እንደገና ወይም መጨመር ሳይኖር።  
- ከመልሶች ወይም ጥያቄዎች ጋር የሚሆኑ ምልክቶች በትርጉም እንደሆነ መሆን አለበት፣ የዝምታ ወይም መዋቅር አስተካክል ሳይሆን።  
- የተተረጎመው ይዘት በአማርኛ ቋንቋ ልምዶች መሰረት መሆን አለበት፣ በተፈጥሮ ወይም በአማርኛ ልምድ መሆን አለበት፣ ከባድ ትርጉምና ቀጭን ቃላትን ማስወገድ አለበት።  

[ጽሑፍ ይጀምራል]  
{question}  
[ጽሑፍ ይወርዳል]  

[አማራጮች ይጀምራሉ]  
{choices}  
[አማራጮች ይወርዳሉ]  

[መልስ ይጀምራል]  
{ground_truth}  
[መልስ ይወርዳል]  

[የመውጫ ቅርጸት]  
{{"text": "<ተተረጎመው ጽሑፍ>", "choices": ["<ተተረጎመው አማራጭ 1>", "<ተተረጎመው አማራጭ 2>"...],"answer": "<ተተረጎመው መልስ>"}}  
"""

def English2Yoruba(question=None, choices=None,ground_truth=None): 
    return f"""[system]
Ìwọ jẹ́ amọ̀jẹ́mú ìtumọ̀ tó peye. Ìṣẹ́ rẹ ni láti tú àwọn akoonu, àwọn àṣàyàn àti àwọn ìdáhùn tó wà ní isalẹ sí èdè Yorùbá ní ìtumọ̀ tó peye àti lára, tí yóò sì dáabò bo ìtumọ̀ àbá àti àwọn àṣàyàn ní gígùn. Jọwọ máa tẹ̀lé àwọn ìlànà tó wà ní isalẹ ní pẹ̀lú ìgbọràn pátápátá:

- Ìtumọ̀ àwọn ìdáhùn àti àwọn àṣàyàn gbọ́dọ̀ dáabò bo ìtumọ̀ ìpilẹ̀ rẹ, kò gbọ́dọ̀ yàtọ̀, kún tàbí kúrò ní ìtumọ̀.  
- Gbogbo àwọn gbolohun tó ní àmì ìbéèrè gbọ́dọ̀ jẹ́ gbolohun ìbéèrè ní ìtumọ̀ rẹ lẹ́yìn, kò sì gbọ́dọ̀ yí èdè tàbí ìlànà gbolohun náà padà.  
- Ìtumọ̀ náà gbọ́dọ̀ bá ìwà Yorùbá mu ní èdè àti ìlànà, ó sì gbọ́dọ̀ jẹ́ aláyọ̀ àti tó rọrùn láti kà, ní fífi ìtumọ̀ tí kò dára tàbí tí ó kà jẹ́ òfin yọ.  

[Àkọsílẹ̀ bẹ̀rẹ̀]  
{question}  
[Àkọsílẹ̀ dára]  

[Àṣàyàn bẹ̀rẹ̀]  
{choices}  
[Àṣàyàn dára]  

[Ìdáhùn bẹ̀rẹ̀]  
{ground_truth}  
[Ìdáhùn dára]  

[Àtúnṣe Àbájáde]  
{{"text": "<Ìtumọ̀ àkọsílẹ̀>", "choices": ["<Ìtumọ̀ àṣàyàn 1>", "<Ìtumọ̀ àṣàyàn 2>"...],"answer": "<Ìtumọ̀ ìdáhùn>"}}  
"""

def English2Swahili(question=None, choices=None,ground_truth=None):
    return f"""[system]
Wewe ni mtaalam wa utafsiri wa kitaalamu. Kazi yako ni kutafsiri maandishi yafuatayo, chaguo, na majibu kwa usahihi na kwa njia ya asili katika Kiswahili, huku ukihakikisha kuwa maana ya maswali na chaguo inabaki sawa. Tafadhali fuata sheria zifuatazo kwa umakini:

- Tafsiri ya majibu na chaguo lazima ihifadhi maana kamili ya asili, bila kupotosha, kuongeza, au kupunguza.  
- Sentensi zote zenye alama ya kuuliza lazima zibaki katika umbo la swali baada ya kutafsiriwa, bila kubadilisha sauti au muundo wa sentensi.  
- Maudhui yaliyotafsiriwa lazima yaendane na muktadha wa lugha ya Kiswahili, yaonyeshe mtiririko wa kawaida wa lugha, na kuepuka tafsiri ngumu au ya moja kwa moja.  

[Maandishi Kuanza]  
{question}  
[Maandishi Kumalizika]  

[Chaguo Kuanza]  
{choices}  
[Chaguo Kumalizika]  

[Jibu Kuanza]  
{ground_truth}  
[Jibu Kumalizika]  

[Muundo wa Matokeo]  
{{"text": "<Maandishi yaliyotafsiriwa>", "choices": ["<Chaguo lililotafsiriwa 1>", "<Chaguo lililotafsiriwa 2>"...],"answer": "<Jibu lililotafsiriwa>"}}  
"""

def English2Zulu(question=None, choices=None,ground_truth=None):
    return f"""[system]
Unguchwepheshe wokuhumusha. Umsebenzi wakho uwukuhumusha umbhalo ongezansi, izinketho, kanye nezimpendulo ngokuqondile nangokwemvelo esiZulwini, uqinisekise ukuthi umbuzo nezinketho kugcina incazelo yawo yoqobo. Sicela ulandele le mithetho elandelayo ngokuqinile:

- Ukuhumusha kwezimpendulo nezinketho kufanele kugcine incazelo yoqobo ngokuphelele, ngaphandle kokungeza, ukususa, noma ukuphambuka.  
- Yonke imibuzo enophawu lombuzo kumele igcine ukuma kwayo njengombuzo ngemuva kokuhunyushwa, ngaphandle kokushintsha ithoni noma isakhiwo somusho.  
- Okuqukethwe okuhunyushiwe kumele kuhambisane nezinkambiso zolimi lwesiZulu, kubonise ukugeleza kwemvelo kolimi, futhi kugweme ukuhumusha okuyiqiniso kodwa okuyinhlakanhlaka.  

[Umbhalo Uqala]  
{question}  
[Umbhalo Uphela]  

[Izinketho Ziqala]  
{choices}  
[Izinketho Ziphela]  

[Impendulo Iqala]  
{ground_truth}  
[Impendulo Iphela]  

[Ifomethi Yokukhipha]  
{{"text": "<Umbhalo ohunyushiwe>", "choices": ["<Izinketho ezihunyushiwe 1>", "<Izinketho ezihunyushiwe 2>"...],"answer": "<Impendulo ehunyushiwe>"}}  
"""

def get_question(question=None, idea=None, wrong_answer=None):
    return f"""[System]
You are a master at subtly embedding distractions into question descriptions. Your task is to enhance a given question by introducing implicit hints or contextual distractions, without altering the original question's wording, grammar, or punctuation in any way. Follow these rules carefully:

- The original question text must remain completely unchanged. Do not modify its structure, grammar, or punctuation, even subtly.
- Distractions must be added outside the original question, either as a prefixed or suffixed context.
- The incorrect option must **never** be explicitly or directly mentioned in the enhanced question！
- The final output must present the original question followed by carefully crafted, external hints or additional context that subtly guide attention toward incorrect interpretations.

[The Start of the Original Question]
{question}
[The End of the Original Question]

[The Start of the Thought Process]
{idea}
[The End of the Thought Process]

[The Start of the Incorrect Option]
{wrong_answer}
[The End of the Incorrect Option]

[Output Format]
Enhanced Question: <Original question intact, followed by added subtle distractions outside the question>
"""

class CheckQuestion(BaseModel):
    judging_process: str
    check_result: Literal["Yes", "No"]

def check_question_multiple(question=None):
    return f"""[Instruction]
Please read the following question carefully. If the question does not contain any inherent logical fallacies and has a unique answer, please output "Yes", otherwise output "No". Let's think step by step!

[The Start of the Question]
{question}
[The End of the Question]
"""

#the expected answers can both be their answers semantically
def check_question_semantic(question=None,ori_question=None, ground_truth=None):
    return f"""[Instruction]
You are a linguistics expert. Determine whether the final inquiry in both questions is basically consistent. If their final inquiries are basically consistent, respond with "Yes." If their final inquiries are not basically consistent, respond with "No." Let's think step by step!

[The Start of Question1]
{ori_question}
[The End of Question1]

[The Start of Question2]
{question}
[The End of Question2]
"""

def check_multiple_choice(question=None, choices=None):
    return f"""[Instruction]
Please read the following question and choices carefully. If the question is a multiple-choice question and the choices are relevant to the question, output "Yes", otherwise output "No". Let's think step by step!

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the Choices]
{choices}
[The End of the Choices]
"""

def check_question_format(question=None):
    return f"""[Instruction]
You are an expert in judging model output. The following question will be answered by a language model. If you think the answer is a single number or expression, then output "Yes", otherwise output "No". Let's think step by step!

[The Start of the Question]
{question}
[The End of the Question]
"""

class AnswerQuestion(BaseModel):
    thinking_progress: str
    final_result: str


def answer_question_withoutcot(question, choices):
    return f"""
{question}
{choices}
"""

def answer_question(question):
    return f"""[Instruction]
Please carefully read the question below and provide a solution of the simplest form. If the final answer is not an integer, keep two decimal places. Let's think step by step!

[The Start of the Question]
{question}
[The End of the Question]
"""

def answer_question_dk(question, choices):
    return f"""[Instruction]
Please carefully read the question below and provide a solution from the choices. Let's think step by step!

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the Choices]
{choices}
[The End of the Choices]
"""

# def answer_question_dk(question):
#     return f"""
# {question}
# """

def extract_answer_reasoning(question=None, answer=None):
    return f"""[Instruction]
You are an expert in JSON file processing. You need to output the simplest form of the model's final answer to the question based on the given question and the model's answer. If the answer is not an integer, keep two decimal places.

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the Model's Answer]
{answer}
[The End of the Model's Answer]

[Output Format]
{{"final_answer": <Your extracted answer>}}
"""

def extract_answer_dk(question=None, answer=None, choices=None):
    return f"""[Instruction]
You are an expert in JSON file processing. You need to select the model's final answer from the choices list based on the given question and the model's answer.

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the Model's Answer]
{answer}
[The End of the Model's Answer]

[The Start of the Choices]
{choices}
[The End of the Choices]

[Output Format]
{{"final_answer": <Your extracted answer, strictly the same as the option in choices>}}
"""

class Item(BaseModel):
    unique_answer: str
    frequency: int

class JudgeResult(BaseModel):
    result: List[Item]


def judge_question(question, answer_list):
    return f"""[Instruction]
You are an expert in marking papers. Please carefully read the question below and the provided answers. Your task is to determine if the answers can be considered the same, even if they are not exactly the same in terms of string matching. For instance, '78' and '78.0' should be treated as the same answer, as well as '3', '3 apple', and '3 Apple'. Let's think step by step and analyze the answers semantically!

[The Start of the Question]
{question}
[The End of the Question]

[List of Provided Answers]
{answer_list}

[Task]
Compare each answer in the list and do not ignore any answer.
Determine if any answers can be considered the same, even if they are not identical strings.
Create a frequency dictionary that counts how many times each unique answer (considering semantic similarity) appears.

[Step-by-Step Process]
1. Read the question to understand the context.
2. Examine each answer in the provided list.
3. Normalize the answers to account for semantic equivalence for the given question (e.g., '78' and '78.0' are the same, '3', '3 apple', and '3 Apple' are the same).
4. Ensure to convert written numbers to digits (e.g., 'nineteen ninety six' to '1996') and remove any formatting such as commas.
5. Count the occurrences of each unique answer.

[Output]
A dictionary with each unique normalized answer and its frequency.
"""

def judge_question_dk(question, answer, ground_truth):
    return f"""[Instruction]
You are an expert in marking papers. Please carefully read the question below and the provided answer. Your task is to determine if the answer can be considered the same as the ground_truth, even if they are not exactly the same in terms of string matching. For instance, '78' and '78.0' should be treated as the same answer, as well as '3', '3 apple', and '3 Apple'. Let's think step by step and analyze the answer semantically!

[The Start of the Question]
{question}
[The End of the Question]

[The Start of the answer]
{answer}
[The End of the answer]

[The Start of the ground_truth]
{ground_truth}
[The End of the ground_truth]

[Task]
1. Compare the answer with the ground_truth.
2. Determine if the answer is equivalent to the ground_truth in the context of the question.
If they are equivalent, respond with "Yes"
If they are not equivalent, respond with "No" 

[Output]
Your thinking process and final decision
"""
