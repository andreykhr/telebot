#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

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
        request = requests.post(URL + TOKEN + '/getUpdates', data=data) # Отправка запроса обновлений
    except:
        log_event('Error getting updates') # Логгируем ошибку
        return False # Завершаем проверку

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id'] # Извлечение ID сообщения

        # Ниже, если в обновлении отсутствует блок 'message'
        # или же в блоке 'message' отсутствует блок 'text', тогда
        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: %s' % update) # сохраняем в лог пришедшее обновление
            continue # и переходим к следующему обновлению
        from_id = update['message']['chat']['id'] # Извлечение ID чата (отправителя)
        name = update['message']['chat']['username'] # Извлечение username отправителя
        if from_id <> ADMIN_ID: # Если отправитель не является администратором, то
            send_text("You're not autorized to use me!", from_id) # ему отправляется соответствующее уведомление
            log_event('Unautorized: %s' % update) # обновление записывается в лог
            continue # и цикл переходит к следующему обновлению
        message = update['message']['text'] # Извлечение текста сообщения
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters) # Вывод в лог ID и текста сообщения

        # В зависимости от сообщения, выполняем необходимое действие
        run_command(*parameters)
