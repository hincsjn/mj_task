from utils import database
from datetime import datetime
from messages import subsription_messages


greeting_msg = '''*Привет\! 👋*

🤖Этот бот работает на технологии нейронных сетей ChatGPT и Midjourney

✔️Создан для того, чтобы решать Ваши текстовые и графические задачи

*Проверяю Вашу историю\.\.\.*🔍'''


def make_menu_message(user_id):
    epoch = int(database.check_users_subscription(user_id, True) / 1000)
    datetime_obj = datetime.utcfromtimestamp(epoch)
    datetime_string=datetime_obj.strftime( "%d\-%m\-%Y" )

    sub_name = database.get_user_attribute(user_id, 'subscription')['name']
    sub_norm_name = subsription_messages.subscriptions[sub_name]['week']['name']

    chat_gpt_functionality = subsription_messages.subscriptions[sub_name]['week']['functionality']['Chat_GPT']
    midjourney_functionality = subsription_messages.subscriptions[sub_name]['week']['functionality']['Midjourney']


    msg = f'''🤖*МЕНЮ*
Ваш тариф: {sub_norm_name}
Доступен до: {datetime_string} 
Текстовых: {chat_gpt_functionality}
Графических: {midjourney_functionality}

*Фишки и кейсы по боту⤵*
https://t\.me/chat\_bot\_v\_tg/15

👇🏼*Выберите режим работы*👇🏼'''
    return msg


first_using_msg = '''
*‼️ВНИМАНИЕ‼️*

Бот временно находится на тех работах\. О возобновлении работы придет сообщение\. Ожидайте пожалуйста

👀*Видим, что вы впервые у нас\!*

Благодарим за то, что решили попробовать нашего бота❤️

*Так как вы впервые*
Мы дарим Вам использование бота без ограничений на 2 дня

После, если вы НЕ перейдете на платные тарифы — Вас переведет автоматически на тариф "Бесплатный"

*✅На нем у Вас будет*
\- 10 текстовых и 4 графических задач в неделю
\- Не будет сохранятся история запросов

*😎Приятного пользования*
Ну а я пока направлю Вас в меню\.\.\.
'''


on_tarif_msg = '''У вас уже активирован тариф "ХХХ" ✅

👉Запускаем?'''


free_tarif_msg = '''👀*Видим, что вы уже пользовались ботом ранее*

С возвращением и приятного пользования! ❤️

*Направляю Вас в меню...*'''


menu_msg = '''🤖 МЕНЮ
Ваш тариф: ххх (базовый/chatgpt/midjourney/все включено)
Доступен до: хх.хх.хххх (у базового тут дата по неделям)
Текстовых: Число / Либо без ограничений
Графических: Число / Либо без ограничений

Выберите режим работы 👇🏼'''


support_msg = '''🕐*Мы отвечаем быстро в рабочее время с пн\-пт 10:00\-19:00 по МСК*

📩Для связи с поддержкой напишите @neural\_help

P\.S\.
Также можете присылать любые рекомендации и доработки ❤️'''


tariffs_msg = '''Оплата 💲

У нас есть 3 тарифа
1. ChatGPT (текстовые задачи) — 349р/мес
2. Midjourney (графические задачи) — 449р/мес
3. Все включено — 649р/мес

Какой тариф выбираете?'''


referal_msg = '''У нас действует 3х уровневая реферальная система
Чтобы изучить подробнее \- нажмите кнопку инструкция

Ваша реферальная ссылка: xxx.ru

Заработано всего: ххх
Выплачено всего: ххх
Текущий баланс: ххх

Приглашенные
1 уровень: х
2 уровень: х
3 уровень: х

Активные подписки:
1 уровень: 7 на сумму ххх
2 уровень: 8 на сумму ххх
3 уровень: 10 на сумму ххх'''


def make_referral_info_msg(user_id):
    ref_data = database.get_referral_data(user_id)
    

    msg = f'''*У нас действует партнерская программа 30%*

*Что это значит:*
Со всех приглашенных вами людей вы будете получать кэшбек 30% от их платежей

*Как происходят выплаты*
По запросу в @neural\_help, от 3000 рублей

*Ваша уникальная ссылка*
`https://t\.me/NeuralAI\_bot?start\={user_id}`
_Кликните, чтобы скопировать_

*Стастистика:*
Приглашенных: {ref_data['count_free']}
Платные пользователи: {ref_data['count_paied']}
Всего заработано: {ref_data['already_payed']+ref_data['remaining_pay']} рублей
Выплачено: {ref_data['already_payed']} рублей
Остаток: {ref_data['already_payed']+ref_data['remaining_pay'] - ref_data['already_payed']}
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

*Для крупных партнеров:*
По запросу в @neural\_help мы можем сделать для вас многоуровневую реферальную систему'''

    return msg