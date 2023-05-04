import redis
import asyncio
import json
from handlers import img_mj_handlers

# r = redis.Redis(
#     host='0.0.0.0',
#     port=6379,
#     password="123",
#     decode_responses=True
# )
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    # password="123",
    decode_responses=True
)
listener = r.pubsub()
listener.subscribe('mj-response')


def proccess_message(message):
    prompt, msg, status = '', '', ''
    if message['t'] == 'MESSAGE_CREATE':
        print('19', message['d']['content'])
        # запрос принят
        if '(Waiting to start)' in message['d']['content']:
            prompt = message['d']['content'].split('**')[1]
            msg = '✅ Запрос принят!'
            status = 'request sent'
        
        # изображение сгенерировано
        elif '(relaxed)' in message['d']['content'] or '(fast)' in message['d']['content']:
            prompt = message['d']['content'].split('**')[1]
            img_link = message['d']['attachments'][0]['url']
            ds_msg_id = message['d']['id']
            msg = f'{img_link} | {ds_msg_id}'
            status = 'response got'
        
        elif 'Image #' in message['d']['content']:
            prompt = message['d']['content'].split('**')[1]
            img_link = message['d']['attachments'][0]['url']
            ds_msg_id = message['d']['id']
            msg = f'{img_link} | {ds_msg_id}'
            status = 'response got upscaled'


        # блок обработки изображения
        # elif 'Image #' in message['d']['content']:


        else:
            # блок ошибок
            try:
                error_title = message['d']['embeds'][0]['title']
                prompt = message['d']['embeds'][0]['footer']['text'].replace('/imagine ', '')

                # использованы запрещенные слова
                if error_title == 'Banned prompt':
                    error_description = message['d']['embeds'][0]['description']
                    banned_word = error_description.split('`')[1]
                    with open('static/stop_word_list.txt', 'a') as f:
                        f.write('\n', banned_word)

                    msg = f'Нарушение правил Midjourney.\nУдалите в запросе слово: {banned_word}'
                    
                
                # запрос попал в очередь
                elif error_title == 'Job queued':
                    error_description = message['d']['embeds'][0]['description']
                    msg = 'Ваш запрос находится в очереди'

                # слишком много запросов в очереди, необходимо повторить позже
                elif error_title == 'Queue full':
                    error_description = message['d']['embeds'][0]['description']

                # ошибка
                else:
                    error_description = message['d']['embeds'][0]['description']
                    msg = 'Возникла непредвиденная ошибка на стороне Midjourney.\nНапишите нам в поддержку @neural_help. И пришлите, пожалуйста, скриншот.'
                    if ':::::' in error_description:
                        exit()
                if msg == '':
                    msg = f'{error_title}\n{error_description}'
                status = 'error'
            
            except:
                ...


    # прогресс генерации изображения
    elif message['t'] == 'MESSAGE_UPDATE':    
        print('58', message['d']['content'])

        if '%' in message['d']['content']:
            percentage = message['d']['content'].split('%)')[0].split('(')[-1]
            msg = f"{int(percentage) // 10 * '🟢' + (10 - int(percentage) // 10) * '⚪️'} {percentage}%"
            prompt = message['d']['content'].split('**')[1]
            status = 'loading'
    
    else:
        return '', '', ''
    

    return prompt, msg, status


async def listen1():
    for message in listener.listen():
        try:
            if message['data'] != '':
                message = json.loads(message['data'])
                # print('77 - message', message)
                try: 
                    if message['t'] in ['MESSAGE_CREATE', 'MESSAGE_UPDATE']:
                        print('80 - message', message)
                except:
                    ...
                prompt, msg, status = proccess_message(message)
                
                if prompt and msg:
                    print('84 - prompt, msg', prompt, msg)
                    if ':::::' in prompt:
                        quit()
                    print()
                    await img_mj_handlers.send_mj_status(prompt, msg, status)
        except TypeError:
            ...
        except KeyError:
            ...
        
    
if __name__ == '__main__':
    asyncio.run(listen1())