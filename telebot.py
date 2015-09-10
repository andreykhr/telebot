#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import ConfigParser
import time
import sys
import os
import random
reload(sys)

sys.setdefaultencoding('utf8')

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

        name = update['message']['chat']['username']

        if from_id <> admin_id:

            runn = api_req(interval,admin_id,api_url,secret,offset,'You\'re not autorized to use me!',from_id)
            data_runn = runn.post_executor()
            log_event('Unautorized: %s' % update)
            continue

        message = update['message']['text']
        log_event('Message from %s: %s' % (name, message))
        answ = messager_test(message)

        if answ:

            runn = api_req(interval,admin_id,api_url,secret,offset,answ,from_id)
            data_runn = runn.post_executor()

config = ConfigParser.RawConfigParser()

try:

    config.read('telebot.cfg')

except:

    print("No config file!")
    exit(0)

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

    if os.path.exists(filename):

        filework = open(filename, 'a')
        filework.write(event)
        filework.write("\n")
        filework.close()

    else:

        filework = open(filename, 'w')
        filework.write(event)
        filework.write("\n")
        filework.close()

def messager_test(message_word):

    words_file = open('words.dat', 'r')

    for strings in words_file:

        list_spl = strings.split("||")

        testword = list_spl[0].strip()

        if message_word == testword:
            rnd = random.randint(1,len(list_spl)-1)
            return list_spl[rnd]

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