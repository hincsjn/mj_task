import json
from typing import Optional
from datetime import datetime

from static.config import *


def check_if_user_exists(user_id: int, raise_exception: bool = False):
    with open(database_path, 'r', encoding='UTF-8')as f:
        database = json.load(f)
        for user in database:
            if user['id'] == user_id:
                return True
        return False


def add_new_user(
        user_id: int,
        chat_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
        referrer_id = None
    ):
    
    user_dict = {
        "id": user_id,
        "chat_id": chat_id,

        "username": username,
        "first_name": first_name,
        "last_name": last_name,

        "last_interaction": datetime.timestamp(datetime.now())*1000,
        "first_seen": datetime.timestamp(datetime.now())*1000,
        
        "current_chat_mode": "assistant",
        'if_answered': None,

        "n_used_tokens": 0,
        'count_imgs': 0,
        'state': 'menu',
        'lang': None,
        'subscription': {'name': None, 'duration': 'free', 'datetime': datetime.timestamp(datetime.now())*1000},
        'referrals': [],
        'referrer_id': referrer_id,
        'already_payed': 0,
        'remaining_pay': 0
    }

    if not check_if_user_exists(user_id):
        with open(database_path, 'r', encoding='UTF-8')as f:
            database = json.load(f)
        print(user_dict)
        database.append(user_dict)

        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False)
        
        start_new_dialog(user_id)


def set_user_attribute(user_id: int, key: str, value):
    with open(database_path, 'r', encoding='UTF-8')as f:
        database = json.load(f)

        for user in database:
            if user['id'] == user_id:
                user[key] = value

    with open(database_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False)
            

def get_user_attribute(user_id: int, key: str):
    with open(database_path, 'r', encoding='UTF-8')as f:
        database = json.load(f)
    
    for user in database:
        if user['id'] == user_id:
            if key not in user:
                set_user_attribute(user_id, key, None)

                return None
            
            return user[key]


def start_new_dialog(user_id: int):
    check_if_user_exists(user_id, raise_exception=True)

    with open(messages_path, 'r', encoding='UTF-8')as f:
        messages = json.load(f)
        
        dialog_id = 0
        for dialog in messages:
            if dialog['user_id'] == user_id:
                dialog_id += 1

        dialog_dict = {
            "id": dialog_id,
            "user_id": user_id,
            "chat_mode": get_user_attribute(user_id, "current_chat_mode"),
            "start_time": datetime.timestamp(datetime.now())*1000,
            "messages": []
        }
        
        messages.append(dialog_dict)

        with open(messages_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False)
        set_user_attribute(user_id, 'current_dialog_id', dialog_id)

    return dialog_id


def set_dialog_messages(user_id: int, dialog_messages: list):
    check_if_user_exists(user_id, raise_exception=True)
    c = 0
    
    with open(messages_path, 'r', encoding='UTF-8')as f:
        messages = json.load(f)

        for dialog in messages:
            if dialog['user_id'] == user_id:
                dialog['messages'] = dialog_messages
                c = 1
        
        if c == 0:
            messages.append({"user_id": user_id, "chat_mode": "assistant", "start_time": datetime.timestamp(datetime.now())*1000, "messages": []})



    with open(messages_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False)
    

def get_dialog_messages(user_id: int):
    check_if_user_exists(user_id, raise_exception=True)


    with open(messages_path, 'r', encoding='UTF-8')as f:
        messages = json.load(f)
        for dialog in messages:
            if dialog['user_id'] == user_id:
                return dialog['messages']
    
    return []


def get_img_attribute(search_key: str, search_value: str, attribute_key: str):
    with open(imgs_path, 'r', encoding='UTF-8') as f:
        imgs = json.load(f)
        print(f'imgs = {imgs}')
        for user in imgs:
            if user[search_key] == search_value:
                return user[attribute_key]
    
    return None


def set_img_attribute(search_key: str, search_value: str, attribute_key: str, attribute_value: Optional[str]):
    with open(imgs_path, 'r', encoding='UTF-8')as f:
        imgs = json.load(f)
        for prompt in imgs:
            if prompt[search_key] == search_value:
                prompt[attribute_key] = attribute_value
                with open(imgs_path, 'w', encoding='utf-8') as f:
                    json.dump(imgs, f, ensure_ascii=False)
                return
            
        imgs.append({search_key: search_value, attribute_key: attribute_value})
        with open(imgs_path, 'w', encoding='utf-8') as f:
            json.dump(imgs, f, ensure_ascii=False)


def set_img_id_attribute(tg_photo_id, mj_photo_id, ds_message_id):
    with open(imgs_id_path, 'r', encoding='UTF-8')as f:
        imgs_id = json.load(f)
        new_dict = {}
        new_dict['tg_photo_id'] = tg_photo_id
        new_dict['mj_photo_id'] = mj_photo_id
        new_dict['ds_message_id'] = ds_message_id
        imgs_id.append(new_dict)

    with open(imgs_id_path, 'w', encoding='utf-8') as f:
        json.dump(imgs_id, f, ensure_ascii=False)
            
        
def get_img_id_attribute(tg_photo_id):
    with open(imgs_id_path, 'r', encoding='UTF-8')as f:
        imgs_id = json.load(f)
        for photo in imgs_id:
            if photo['tg_photo_id'] == tg_photo_id:
                mj_photo_id = photo['mj_photo_id']
                ds_message_id = photo['ds_message_id']
                return tg_photo_id, mj_photo_id, ds_message_id


def get_user_id_by_filename(filename: str, like_file_path=True):
    with open(imgs_path, 'r', encoding='UTF-8')as f:
        imgs = json.load(f)
        print(f'imgs -- {imgs}')
        if imgs != []:
            for user in imgs:
                prompt = user['prompt']
                if like_file_path:
                    while ' ' in prompt:
                        prompt = prompt.replace(' ', '_')
                try:
                    if prompt[:30] in filename:
                        return user['id']
                except:
                    if prompt in filename:
                        return user['id']
                    

def get_img_name(request:str):
    with open(imgs_path, 'r', encoding='UTF-8')as f:
        imgs = json.load(f)

        print(f'imgs -- {imgs}')
        if imgs != []:
            for user in imgs:
                prompt = user['prompt']
                if prompt == request:
                    return user['user_id']


def delete_last_prompt(user_id: int):
    with open(imgs_path, 'r', encoding='UTF-8')as f:
        imgs = json.load(f)
    
    for prompt in imgs:
        if prompt['user_id'] == user_id and prompt['status'] == 'successfully_sent_to_tg':
            imgs.remove(prompt)
    

    with open(imgs_path, 'w', encoding='utf-8') as f:
        json.dump(imgs, f, ensure_ascii=False)


    with open(database_path, 'r', encoding='UTF-8')as f:
        database = json.load(f)
        for user in database:
            if user['id'] == user_id:
                try:
                    user['count_imgs'] += 1
                except:
                    user['count_imgs'] = 1

    with open(database_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False)