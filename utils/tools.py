import os
import functools
import time
import re
import json
import logging
import tiktoken
import anthropic
from dotenv import load_dotenv
from openai import OpenAI
from functools import wraps

load_dotenv()

os.environ['http_proxy'] = os.getenv('HTTP_PROXY')
os.environ['https_proxy'] = os.getenv('HTTPS_PROXY')

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Change to INFO to reduce log verbosity
    format='%(message)s',
    handlers=[
        logging.FileHandler("run.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Reduce verbosity of third-party libraries
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)

class TokenLogger:
    def __init__(self, filename="token_original.txt"):
        self.filename = filename
        self.model_tokens = {}
        self.load_tokens()

    def log_tokens(self, model_name, input_tokens, output_tokens):
        if model_name not in self.model_tokens:
            self.model_tokens[model_name] = {"input_total": 0, "output_total": 0, "last_input": 0, "last_output": 0}
        
        self.model_tokens[model_name]["input_total"] += input_tokens
        self.model_tokens[model_name]["output_total"] += output_tokens
        self.model_tokens[model_name]["last_input"] = input_tokens
        self.model_tokens[model_name]["last_output"] = output_tokens

        self.save_tokens()

    def get_total_tokens(self, model_name):
        if model_name in self.model_tokens:
            return self.model_tokens[model_name]["input_total"], self.model_tokens[model_name]["output_total"]
        else:
            return 0, 0

    def save_tokens(self):
        with open(self.filename, 'w') as file:
            for model_name, tokens in self.model_tokens.items():
                file.write(f"{model_name},{tokens['input_total']},{tokens['output_total']},{tokens['last_input']},{tokens['last_output']}\n")

    def load_tokens(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    model_name, input_total, output_total, last_input, last_output = line.strip().split(',')
                    self.model_tokens[model_name] = {
                        "input_total": int(input_total),
                        "output_total": int(output_total),
                        "last_input": int(last_input),
                        "last_output": int(last_output)
                    }
        else:
            self.model_tokens = {}

token_logger = TokenLogger()

def num_tokens_from_string(string: str, encoding_name='cl100k_base') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    logger.warning(f"Exception occurred: {e}")

                retries += 1
                logger.info(f"Retrying ({retries}/{max_retries}) in {current_delay} seconds...")
                time.sleep(current_delay)
                current_delay *= backoff
            return None
        return wrapper_retry
    return decorator_retry

def token_logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        model_name = args[0] if len(args) > 0 else kwargs.get('model', '')
        prompt = args[1] if len(args) > 1 else kwargs.get('prompt', '')
        
        input_tokens = num_tokens_from_string(prompt)
        response = func(*args, **kwargs)
        output_tokens = num_tokens_from_string(response)
        token_logger.log_tokens(model_name, input_tokens, output_tokens)
        return response
    return wrapper

model_dict = {
    'gpt-4o': 'gpt-4o',
    'gpt-4o-mini': 'gpt-4o-mini',
    'o1-mini': 'o1-mini-2024-09-12',
    'chatgpt-4o-latest': 'chatgpt-4o-latest',
    'llama-3.1-70B': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
    'llama-3.1-8B': 'meta-llama/Meta-Llama-3.1-8B-Instruct',
    'gemma-2-27B': 'google/gemma-2-27b-it',
    'gemma-2-9B': 'google/gemma-2-9b-it',
    'qwen-2.5-72B': 'Qwen/Qwen2.5-72B-Instruct',
    'qwen-2.5-32B': 'Qwen/Qwen2.5-32B-Instruct',
    'qwen-2.5-14B': 'Qwen/Qwen2.5-14B-Instruct',
    'qwen-2.5-7B': 'Qwen/Qwen2.5-7B-Instruct',
    'yi-lightning': 'yi-lightning',
    'claude-3.5-sonnet': 'claude-3-5-sonnet-20241022'
}

@retry_on_failure()
@token_logger_decorator
def get_response(model='chatgpt-4o-latest', prompt=None, temperature=0.001):
    if model in ['claude-3.5-sonnet']:
        client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        message = client.messages.create(
            model=model_dict[model],
            max_tokens=2048,
            temperature=temperature,
            system='You are a helpful assistant.',
            messages=[{'role': 'user', 'content': [{'type': 'text', 'text': prompt}]}]
        )
        return message.content[0].text
    if model in ['llama-3.1-70B', 'llama-3.1-8B', 'qwen-2.5-72B', 'gemma-2-27B']:
        client = OpenAI(
            api_key=os.getenv('DEEPINFRA_API_KEY'),
            base_url=os.getenv('DEEPINFRA_BASE_URL')
        )
    elif model == 'yi-lightning':
        client = OpenAI(
            api_key=os.getenv('YI_API_KEY'),
            base_url=os.getenv('YI_BASE_URL')
        )
    else:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if model in ['o1-mini']:
        messages = [{'role': 'user', 'content': prompt}]
        response = client.chat.completions.create(
            model=model_dict[model],
            messages=messages,
        )
        return response.choices[0].message.content
    messages = [{"role": 'system', "content": "You are a helpful assistant."}]
    messages.append({'role': 'user', 'content': prompt})
    
    response = client.chat.completions.create(
        model=model_dict[model],
        messages=messages,
        temperature=temperature,
    )

    result_content = response.choices[0].message.content
    return result_content

@retry_on_failure()
@token_logger_decorator
def get_structured_response(model='gpt-4o', prompt=None, history=[], temperature=0.5, response_format=None):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    messages = [{"role": message['role'], "content": message['content']} for message in history]
    messages.append({'role': 'user', 'content': prompt})
    # messages.insert(0, {"role": "system", "content": "You are a skilled math probelm solver. Solve the following problem step by step."})

    response = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format=response_format
    )

    result_content = response.choices[0].message.parsed
    return result_content.model_dump_json(indent=4)

def extract_string_between_bars(s):
    pairs = []
    start = s.find('||')
    while start != -1:
        end = s.find('||', start + 2)
        if end != -1:
            pairs.append((start, end))
            start = s.find('||', end + 2)
        else:
            break
    if not pairs:
        return None
    
    last_pair = pairs[-1]
    result = s[last_pair[0] + 2:last_pair[1]]
    return result

def extract_json_between_bars(text):

    def unescape_string(s):
        s = s.replace('\\\\', '\\').replace('\\"', '"').replace("\\'", "'")
        return re.sub(r'\\(.)', r'\1', s)

    def try_json_load(content):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                content = unescape_string(content)
                return json.loads(content)
            except json.JSONDecodeError:
                return None

    match = re.findall(r'\|\|([^|]+)\|\|', text)
    
    if not match:
        return None

    last_content = match[-1].strip()
    result = try_json_load(last_content)
    return result

def clear_json(text):
    try:
        text = re.sub(r'```json\n(.+?)```', r'\1', text, flags=re.DOTALL)
    except:
        pass
    return text

def num_tokens_from_string(string: str, encoding_name='cl100k_base') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens   