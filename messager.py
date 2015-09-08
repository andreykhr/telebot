#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def messager_test(message_word):

    print(message_word)

    words_file = open('words.dat', 'r')

    for strings in words_file:

        list_spl = strings.split("||")

        testword = list_spl[0].strip()

        if message_word == testword:
            rnd = random.randint(1,len(list_spl)-1)
            return list_spl[rnd]