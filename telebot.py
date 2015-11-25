#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, ConfigParser, time, sys, os, random, string

reload(sys)

sys.setdefaultencoding('utf-8')

class api_req:

    def __init__(self,interval,admin_id,api_url,secret,offset,text,chat_id):

        self.interval=interval
        self.admin_id=admin_id
        self.api_url=api_url
        self.secret=secret
        self.offset=offset
        self.text=text
        self.chat_id=chat_id

    def request_executor(self):

        self.options={'offset': self.offset + 1, 'limit': 5, 'timeout': 0}

        try:

            self.request = requests.get(self.api_url + self.secret + '/getUpdates', data=self.options)

        except:

            print('Error getting updates')
            return False

        if not self.request.status_code == 200: return False
        if not self.request.json()['ok']: return False

        return self.request.json()['result']

    def post_executor(self):

        log_event('Sending to %s: %s' % (self.chat_id, self.text))
        self.options={'chat_id': self.chat_id, 'text': self.text}
        self.request=requests.post(self.api_url + self.secret + '/sendMessage',self.options)
        if not self.request.status_code == 200:

            return False
        return self.request.json()['ok']

def message_extraction(message_body):

    global offset

    for update in message_body:

        offset = update['update_id']

        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: %s' % update)
            continue

        from_id = update['message']['chat']['id']
        chat_number = update['message']['from']['id']

        if not 'first_name' in update['message']['from']:
            name = update['message']['from']['last_name']
            print name
        if not 'last_name' in update['message']['from']:
            name = update['message']['from']['first_name']
        else:
            name =  update['message']['from']['first_name'] + ' ' + update['message']['from']['last_name']
        message = update['message']['text']
        log_event('Message from %s: %s' % (name, message))
        answ = messager_test(message)

        if answ:

            runn = api_req(interval,admin_id,api_url,secret,offset,answ,from_id)
            data_runn = runn.post_executor()

config = ConfigParser.RawConfigParser()

config.read('telebot.cfg')

try:
    
    interval = config.getfloat('SectionBot', 'interval')
    admin_id = config.getint('SectionBot', 'admin_id')
    api_url = config.get('SectionBot', 'api_url')
    secret = config.get('SectionBot', 'secret')
    offset = config.getint('SectionBot', 'offset')
    text='Hello'
    chat_id=0

except:

    print("Can't parse config file!")
    exit(0)

def log_event(text):

    filename = 'chat_log.txt'

    event = '%s >> %s' % (time.ctime(), text)

    filework = open(filename, 'a+')
    filework.write(event)
    filework.write("\n")
    filework.close()

def messager_test(message_word):

    if message_word == '/help':

        return "Telebot - Simple Telegram bot"

    elif message_word == '/stop':

        return "Hui tebe!"

    elif message_word == '/start':

        return "OK"

    try:

        words_file = open('words.dat', 'r')

    except:

        print "Can't open words file!"
        exit(0)

    message_word = message_word.encode('utf-8', 'ignore') # Извлекаем слово, убираем пунктуацию, переводим в нижний регистр и загоняем в список по пробелам
    message_word_truncated = message_word.translate(string.maketrans("",""), string.punctuation).decode('utf-8').lower().split(" ")
    string_with_words = []

    for strings in words_file:

        counter = 0
        list_original = strings.split(" || ")
        list_spl = strings.lower().split(" || ") # Получаем строку из файла, делим ее по разделителю и переводим в нижний регистр
        list_spl_truncated = list_spl[:]

        for elements in list_spl:

            list_spl_truncated[counter] = list_spl[counter].translate(string.maketrans("",""), string.punctuation) #  Удаляем пунктуацию, получаем чистый список
            counter+=1

        list_diff = list(set(list_spl_truncated) & set(message_word_truncated)) #  получаем точки пресечения списков

        if list_diff:

            string_with_words = string_with_words + list_original

    if string_with_words:

        rnd = random.randint(1,len(string_with_words)-1)
        answ_word = string_with_words[rnd]

        return answ_word

    else:

        return False

if __name__ == "__main__":
    while True:

        try:
            test = api_req(interval,admin_id,api_url,secret,offset,text,chat_id)
            data_test = test.request_executor()
            message_extraction(data_test)
            time.sleep(interval)
        except KeyboardInterrupt:
            print 'Прервано пользователем..'
            break