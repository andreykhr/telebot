#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import ConfigParser

#interval = 3
#admin_id = 400793
#api_url = 'https://api.telegram.org/bot'
#secret = '96873572:AAGB7UU19Lo9OTQBd6K6lBeXwZSfzy-LXZE'
#offset = 543796984

class api_post:   # Отправка сообщения

    def __init__(self, api_url, secret, chat_id, text):

        self.api_url=api_url
        self.secret=secret
        self.chat_id=chat_id
        self.text=text

    def message_generator(self):

        self.options = {'chat_id': chat_id, 'text': text}
        return self.options

    def message_post(self):

        log_event('Sending to %s: %s' % (chat_id, text))
        self.request = requests.post(self.api_url + self.secret + '/sendMessage', data=message_generator())
        if not self.request.status_code == 200:
            return False
        return self.request.json()['ok']

class api_req:

    def __init__(self,interval,admin_id,api_url,secret,offset):

        self.interval=interval
        self.admin_id=admin_id
        self.api_url=api_url
        self.secret=secret
        self.offset=offset

  #  def request_generator(self):    # Метод генерирует строку опций для запроса

      #self.options={'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
   #     return self.options

    def request_executor(self):     # Берем строку из request_generator и выполняем запрос

        self.options={'offset': self.offset + 1, 'limit': 5, 'timeout': 0}

        try:

            self.request = requests.get(self.api_url + self.secret + '/getUpdates', data=self.options)
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

def debugging_run_post():

    post_info = apt_post(api_url, secret, from_id, text)

def message_extraction(message_body):

    for update in message_body:

        offset = update['update_id']

        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: %s' % update) # сохраняем в лог пришедшее обновление
            continue

        from_id = update['message']['chat']['id']

        name = update['message']['chat']['username']

        if from_id <> admin_id:
            send_text("You're not autorized to use me!", from_id)
            log_event('Unautorized: %s' % update)
            continue

        message = update['message']['text']

     #   print offset

     #   print message      пока отладка - пусть будет.

     #   print from_id

     #   print name

        ret={'offset': offset, 'message': message, 'from_id': from_id, 'name': name}

     #   return ret


def log_event(text):

    event = '%s >> %s' % (time.ctime(), text)
    print event



config = ConfigParser.RawConfigParser()
config.read('/Users/one/Documents/Code/test/telebot.cfg')

interval = config.get('SectionBot', 'interval')
admin_id = config.get('SectionBot', 'admin_id')
api_url = config.get('SectionBot', 'api_url')
secret = config.get('SectionBot', 'secret')
offset = config.get('SectionBot', 'offset')

print interval
print admin_id
print api_url
print secret
print offset


rebzya = debugging_run()
otvet = message_extraction(rebzya)


# print rebzya