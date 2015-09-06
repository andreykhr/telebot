#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

#params='additional'
#state='true'

class inspector:

    def __init__(self,params,state):

        self.params=params
        self.state=state

    def inspection_generator(self):

        self.inspection = {'params': self.params, 'state': self.state }

        return self.inspection


def return_opt():

    move_dat = inspector('aditional','true')
    ask_ret = move_dat.inspection_generator()
    return ask_ret

d = return_opt()
print(d)