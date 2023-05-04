

discord_token = ''
ds_login = ''
ds_pass = ''
telegram_token = ''

openai_api_key = ''

use_chatgpt_api = True
allowed_telegram_usernames = []
admin_usernames = []
test_mail_list = []

messages_path = 'static/messages.json'
database_path = 'static/database.json'
imgs_path = 'static/imgs.json'
imgs_id_path = 'static/img_ids.json'
stop_word_list_path = 'static/stop_word_list.txt'
discord_user_token_path = 'static/discord_user_token.txt'

chat_gpt_tariff_month = 349
img_mj_tariff_month = 449
all_tariff_month = 649

chat_gpt_tariff_week = 99
img_mj_tariff_week = 149
all_tariff_week = 199

new_dialog_timeout = 600000
enable_message_streaming = False

chat_modes = {
    'assistant':{
        'name': '👩🏼‍🎓 General Assistant',
        'welcome_message': "👩🏼‍🎓 Hi, I'm <b>ChatGPT general assistant</b>. How can I help you?",
        'prompt_start': """As an advanced chatbot named ChatGPT, your primary goal is to assist users to the best of your ability. This may involve answering questions, providing helpful information, or completing tasks based on user input. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user.""",
        'parse_mode': 'html'
    },
    'any-ru': {
        'name': '',
        'welcome_message': '',
        'prompt_start': 'I want you to act as an Russian translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in Russian. I want you to replace my simplified words and sentences with more beautiful and elegant, upper level Russian words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations'
    },
    'any-eng': {
        'name': '',
        'welcome_message': '',
        'prompt_start': 'I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations'
    }
}