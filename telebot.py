#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import ConfigParser
import time
import sys
import os
import random
import string

reload(sys)

sys.setdefaultencoding('utf-8')


class api_req:  # Класс для get/post из telegram api

    def __init__(self,interval,admin_id,api_url,secret,offset,text,chat_id,chat_name):

        self.interval = interval
        self.admin_id = admin_id
        self.api_url = api_url
        self.secret = secret
        self.offset = offset
        self.text = text
        self.chat_id = chat_id
        self.chat_name = chat_name

    def request_executor(self):

        self.options = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}

        try:

            self.request = requests.get(self.api_url + self.secret + '/getUpdates', data=self.options)

        except:

            print('Error getting updates')
            return False

        if not self.request.status_code == 200:

            return False

        if not self.request.json()['ok']:

            return False

        if self.request.json()['result']:

            return self.request.json()['result']

        else:

            return False

    def post_executor(self):

        log_event('Sending to %s: %s' % (self.chat_name, self.text), self.chat_name)
        self.options = {'chat_id': self.chat_id, 'text': self.text}
        self.request = requests.post(self.api_url + self.secret + '/sendMessage', self.options)

        if not self.request.status_code == 200:

            return False

        return self.request.json()['ok']


def message_extraction(message_body):  # Выковыриваем из ответа сообщение

    if type(message_body) == str or int:  # Иногда приезжает булевый тип данных, ломая итерацию. Избавляемся.

        global offset

        for update in message_body:

            offset = update['update_id']

            if not 'message' in update or not 'text' in update['message']:

                log_event('Unknown update: %s' % (update), "error")
                continue

            from_id = update['message']['chat']['id']
            chat_number = update['message']['chat']['id']
            chat_type = update['message']['chat']['type']

            if not 'first_name' in update['message']['from']:   # Проверка наличия имени и фамилии пользователя, они не всегда бывают.

                name = update['message']['from']['last_name']
                print(name)

            if not 'last_name' in update['message']['from']:

                name = update['message']['from']['first_name']

            else:

                name = update['message']['from']['first_name'] + ' ' + update['message']['from']['last_name']

            if chat_type == "group":    # Определяем имя чата для последующей записи в лог.

                chat_name = update['message']['chat']['title']

            elif chat_type == "private":

                chat_name = name

            message = update['message']['text']  # Вытаскиваем текст сообщения.

            log_event('Message from %s: %s' % (name, message), chat_name)

            return (message, from_id, chat_name, chat_number)  # Возвращаем сообщение и идентификаторы чата


config = ConfigParser.RawConfigParser()

config.read('telebot.cfg')

try:

    interval = config.getfloat('SectionBot', 'interval')
    admin_id = config.getint('SectionBot', 'admin_id')
    api_url = config.get('SectionBot', 'api_url')
    secret = config.get('SectionBot', 'secret')
    offset = config.getint('SectionBot', 'offset')
    lock_file = 'tmp/telebot.lock'
    text = 'Hello'
    chat_id = 0

except:

    print("Can't parse config file!")
    exit(0)


def log_event(text, logname):

    filename = 'chatlogs/'+logname+'_log.txt'

    event = '%s >> %s' % (time.ctime(), text)

    filework = open(filename, 'a+')
    filework.write(event)
    filework.write("\n")
    filework.close()


def learner(message_text, chat_number):

    chat_number = str(chat_number)
    chat_number = chat_number.replace('+', '').replace('-','')
    message_text = message_text.replace('/learn','').strip()
    filework = open('dict/' + chat_number + '_words.dat', 'a')
    filework.write(message_text)
    filework.write("\n")
    filework.close()


def messager_test(message_word,chat_name,chat_number):

    message_word_command = message_word.split(" ")

    if message_word_command[0] == '/help':

        return "Telebot - Simple Telegram bot"

    elif message_word_command[0] == '/stop':

        return "Hui tebe!"

    elif message_word_command[0] == '/start':

        return "OK"

    elif message_word_command[0] == '/learn':

        learner(message_word, chat_number)
        return "Зопейсал"

    try:
        chat_number = str(chat_number)
        chat_number = chat_number.replace('+', '').replace('-', '')
        words_file = open('dict/' + chat_number + '_words.dat', 'r')

    except:

        return False

    message_word = message_word.encode('utf-8', 'ignore')  # Извлекаем слово, убираем пунктуацию, переводим в нижний регистр и загоняем в список по пробелам
    message_word_truncated = message_word.translate(string.maketrans("",""), string.punctuation).decode('utf-8').lower().split(" ")
    string_with_words = []

    for strings in words_file:

        counter = 0
        list_original = strings.split(" || ")
        list_spl = strings.decode('utf-8').lower().split(" || ")  # Получаем строку из файла, делим ее по разделителю и переводим в нижний регистр
        list_spl_truncated = list_spl[:]

        for elements in list_spl:

            list_spl_truncated[counter] = list_spl[counter].encode('utf-8', 'ignore').translate(string.maketrans("",""), string.punctuation).decode('utf-8')  # Удаляем пунктуацию, получаем чистый список
            counter += 1

        list_diff = list(set(list_spl_truncated) & set(message_word_truncated))  # получаем точки пресечения списков

        if list_diff:

            string_with_words = string_with_words + list_original  # Собираем значения, совпавшие со строками списков в один список.

    if string_with_words:

        rnd = random.randint(1, len(string_with_words)-1)  # Из образовавшегося набора рандомно выбираем фразу или слово, как повезет.

        words_file.close()

        return string_with_words[rnd]

    else:

        return False

if __name__ == "__main__":

    if os.path.exists(lock_file):

        print('Lock file exists!')
        #exit(0)

    else:

        try:

            open(lock_file, 'a+')
            lock_file.close()

        except:

            exit(0)

    while True:

        try:

            chat_name = 0
            answ_data = False
            message_data = False
            test = api_req(interval, admin_id, api_url, secret, offset, text, chat_id, chat_name)

            data_test = test.request_executor()

            if data_test:

                message_data = message_extraction(data_test)

            if message_data:

                message, from_id, chat_name, chat_number = message_data
                answ = messager_test(message, chat_name, chat_number)

                if answ:

                    runn = api_req(interval, admin_id, api_url, secret, offset, answ, from_id, chat_name)
                    runn.post_executor()

            time.sleep(interval)

        except KeyboardInterrupt:

            print('Прервано пользователем..')
            os.remove('lock_file')
            break
