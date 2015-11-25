#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import telebot
from daemonize import Daemon

class MyDaemon(Daemon):
    def run(self):
        telebot.start()

if __name__ == "__main__": 
    my_daemon = MyDaemon('telebot.pid')

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            print 'starting telebot'
            my_daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'stoping telebot'
            my_daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'restarting telebot'
            my_daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)