#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

interval = 3
admin_id = 400793
api_url = 'https://api.telegram.org/bot'
secret = '96873572:AAGB7UU19Lo9OTQBd6K6lBeXwZSfzy-LXZE'
offset = 0

class api_req:

    def __init__(self,interval,admin_id,api_url,secret,offset):

        self.interval=interval
        self.admin_id=admin_id
        self.api_url=api_url
        self.secret=secret
        self.offset=offset

    def request_generator(self):    # Метод генерирует строку опций для запроса

        self.options={'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        return self.options

    def request_executor(self):     # Берем строку из request_generator и выполняем запрос

        try:

            self.request = requests.get(self.api_url + self.secret + '/getUpdates', data=self.request_generator())
            print self.request

        except:

            print('Error getting updates')
            return False

        if not self.request.status_code == 200: return False
        if not self.request.json()['ok']: return False
                                    # Произвели проверки ответа
        return self.request.json()['result']
                                    # Вернули содержимое json в блоке result

def debugging_run():

    debug_info = api_req(interval,admin_id,api_url,secret,offset)
    data_new = debug_info.request_executor()
    return data_new   # Вызвали метод request_executor из класса api_req, получили result и вернули его

def message_extraction(message_body):

    for update in message_body:

        offset = update['update_id']

        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: %s' % update) # сохраняем в лог пришедшее обновление
            continue

        from_id = update['message']['chat']['id']

        message = update['message']['text']

        name = update['message']['chat']['username']

        print offset

        print message

        print from_id

# global offset = 0# пока пусть будет глобальным, а то хз


rebzya = debugging_run()
otvet = message_extraction(rebzya)
# print rebzya
