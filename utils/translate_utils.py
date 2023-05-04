import tiktoken
import openai

from static import config


openai.api_key = config.openai_api_key
CHAT_MODES = config.chat_modes

OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "max_tokens": 2500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}


def generate_prompt_messages_for_chatgpt_api_translate(message, dialog_messages, chat_mode):
    prompt = CHAT_MODES[chat_mode]["prompt_start"]

    messages = [{"role": "system", "content": prompt}]

    if chat_mode == 'any-eng':
        messages.append({"role": "user", "content": 'translate this in English "' + message + '"'})
    else:
        messages.append({"role": "user", "content": 'переведи этот текст на русский "' + message + '"'})

    return messages


async def translate(message, dialog_messages=[], chat_mode='assistant', lang=None):
    n_dialog_messages_before = len(dialog_messages)
    answer = None
    if lang == 'ru':
        chat_mode = 'any-ru'
    elif lang == 'eng':
        chat_mode = 'any-eng'

    while answer is None:
        try:
            messages = generate_prompt_messages_for_chatgpt_api_translate(message, dialog_messages, chat_mode)

            r = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                **OPENAI_COMPLETION_OPTIONS
            )

            answer = r.choices[0].message['content']

            answer = postprocess_answer(answer)
            n_used_tokens = r.usage.total_tokens

        except openai.error.InvalidRequestError as e:
            if len(dialog_messages) == 0:
                raise ValueError("Dialog messages is reduced to zero, but still has too many tokens to make completion") from e

            dialog_messages = dialog_messages[1:]

    n_first_dialog_messages_removed = n_dialog_messages_before - len(dialog_messages)

    return answer, n_used_tokens, n_first_dialog_messages_removed


def postprocess_answer(answer):
    answer = answer.strip()
    return answer


def count_tokens_for_chat_gpt(prompt_messages, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    n_tokens = 0
    for message in prompt_messages:
        n_tokens += 4  
        for key, value in message.items():            
            if key == "role":
                n_tokens += 1
            elif key == "content":
                n_tokens += len(encoding.encode(value))
            else:
                raise ValueError(f"Unknown key in message: {key}")
                
    n_tokens -= 1 
    return n_tokens
