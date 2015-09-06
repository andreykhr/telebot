#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import subprocess
import os


requests.packages.urllib3.disable_warnings()

INTERVAL = 3
ADMIN_ID = 400793
URL = 'https://api.telegram.org/bot'
TOKEN = '96873572:AAGB7UU19Lo9OTQBd6K6lBeXwZSfzy-LXZE'
offset = 0

def check_updates():
    """Проверка обновлений на сервере и инициация действий, в зависимости от команды"""
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0} # Формируем параметры запроса

    try:
        print "Sending request"
        request = requests.get(URL + TOKEN + '/getUpdates', data=data) # Отправка запроса обновлений
    except:
        log_event('Error getting updates') # Логгируем ошибку
        return False # Завершаем проверку

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id'] # Извлечение ID сообщения
        print "Offset ",offset
        message = update['message']['text']
        print "Message", message


if __name__ == "__main__":
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print 'Прервано пользователем..'
            break