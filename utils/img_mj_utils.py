import time
import requests
from utils import database
from static.config import discord_user_token_path, ds_login, ds_pass


def read_token():
    with open(discord_user_token_path, 'r', encoding='UTF-8')as f:
        token = f.read()
    return token


def calculateNonce(date="now"):
        if date == "now":
            unixts = time.time()
        else:
            unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)
    

def update_token():
    log_url = 'https://discord.com/api/v9/auth/login'
    login_headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/login',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'ru',
        'x-fingerprint': '1091548785311764540.ZkcPaBIkOVLmyfdYrbHMbf3C7Dk',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1LVJVIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly9saW51eGhpbnQuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6ImxpbnV4aGludC5jb20iLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxODU3NTgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0=',
    }

    login_payload = {
        'login': ds_login,
        'password': ds_pass,
        "undelete":'false',
        "captcha_key":'null',
        "login_source":'null',
        "gift_code_sku_id":calculateNonce()
    }

    r = requests.post(log_url, headers=login_headers, json=login_payload)
    try:
        token = r.json()['token']
    except:
        print('Не удалось получить новый дискорд токен, ох ебала')
    with open(discord_user_token_path, 'w', encoding='UTF-8')as f:
        f.write(token)


def send_response_midjourney(prompt):
    mj_response_payload = {
        "type":2,
        "application_id":"936929561302675456",
        "guild_id":"1091548248910614579",
        "channel_id":"1091548249371975770",

        "session_id":"f0bad1f20092eb961bf791b82e69b627",
        "data":{
            "version":"1077969938624553050",
            "id":"938956540159881230",
            "name":"imagine",
            "type":1,
            "options":[{"type":3,"name":"prompt","value":prompt}],
            "application_command":{
                "id":"938956540159881230",
                "application_id":"936929561302675456",
                "version":"1077969938624553050",
                "default_permission":"true",
                "default_member_permissions":"null",
                "type":1,
                "nsfw":"false",
                "name":"imagine",
                "description":"Create images with Midjourney",
                "dm_permission":"true",
                "options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":"true"}]},
                "attachments":[]
            },"nonce":calculateNonce()
    }

    
    url = 'https://discord.com/api/v9/interactions'
    with requests.Session() as client:
        mj_response_header = {
            'authorization': read_token()
        }   

        r = client.post(url, headers=mj_response_header, json=mj_response_payload)
        print(r.text)

        if r.status_code == 204:
            print(f'Successfully sent prompt: {prompt}')
            return True
        elif r.status_code > 400:
            update_token()
            mj_response_header = {
                'authorization': read_token()
            }
            r = client.post(url, headers=mj_response_header, json=mj_response_payload)
            if r.status_code == 204:
                print(f'Successfully sent prompt: {prompt}')
                return True

        else:
            time.sleep(r.json()['retry_after']+1)
            r = client.post(url, headers=mj_response_header, json=mj_response_payload)
            if r.status_code == 204:
                print(f'Successfully sent prompt: {prompt}')
                return True
        
        return False


def process_mj_imj(type, tg_photo_id, number:int):
    tg_photo_id, mj_photo_id, ds_message_id = database.get_img_id_attribute(tg_photo_id)
    mj_response_header = {
        'authorization': read_token()
    } 
    if type == 'reroll':
        custom_id = f'MJ::JOB::{type}::{number}::{mj_photo_id}::SOLO'
    else:
        custom_id = f'MJ::JOB::{type}::{number}::{mj_photo_id}'

    payload = {
        'type': 3,
        'nonce': calculateNonce(),
        'guild_id': '1091548248910614579',
        'channel_id': '1091548249371975770',
        'message_flags': 0,
        'message_id': str(ds_message_id),

        'application_id': '936929561302675456',
        'session_id': '2ab251712260f75953fa886bc37f146f',
        'data': {
            'component_type': 2,
            'custom_id': custom_id,
        },
    }
    
    url = 'https://discord.com/api/v9/interactions'
    with requests.Session() as client:
        mj_response_header = {
            'authorization': read_token()
        }   

        r = client.post(url, headers=mj_response_header, json=payload)
        print(r.text)

        if r.status_code == 204:
            print(f'Successfully sent "variations": {tg_photo_id, number}')
            return True
        elif r.status_code > 400:
            update_token()
            mj_response_header = {
                'authorization': read_token()
            }
            r = client.post(url, headers=mj_response_header, json=payload)
            if r.status_code == 204:
                print(f'Successfully sent "variations": {tg_photo_id, number}')
                return True

        else:
            print(r.json())
            time.sleep(r.json()['retry_after']+1)
            r = client.post(url, headers=mj_response_header, json=payload)
            if r.status_code == 204:
                print(f'Successfully sent "variations": {tg_photo_id, number}')
                return True
        
        return False
    
