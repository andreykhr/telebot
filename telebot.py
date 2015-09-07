#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import ConfigParser
import time

class api_req:

    def __init__(self,interval,admin_id,api_url,secret,offset):

        self.interval=interval
        self.admin_id=admin_id
        self.api_url=api_url
        self.secret=secret
        self.offset=offset

    def request_executor(self):

        self.options={'offset': self.offset + 1, 'limit': 5, 'timeout': 0} # Генерация строки параметров

        try:

            self.request = requests.get(self.api_url + self.secret + '/getUpdates', data=self.options) # Запрос

        except:

            print('Error getting updates')
            return False

        if not self.request.status_code == 200: return False
        if not self.request.json()['ok']: return False
                                    # Произвели проверки ответа
        return self.request.json()['result']


config = ConfigParser.RawConfigParser()
config.read('/Users/one/Documents/Code/test/telebot.cfg')

interval = config.getfloat('SectionBot', 'interval')
admin_id = config.get('SectionBot', 'admin_id')
api_url = config.get('SectionBot', 'api_url')
secret = config.get('SectionBot', 'secret')
offset = config.getint('SectionBot', 'offset')


if __name__ == "__main__":
    while True:
        try:
            test = api_req(interval,admin_id,api_url,secret,offset)
            data_test = test.request_executor()
            print data_test
            time.sleep(interval)
        except KeyboardInterrupt:
            print 'Прервано пользователем..'
            break