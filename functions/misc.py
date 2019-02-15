#!/usr/bin/env python3
# encoding=utf-8

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import debug

def createCallbackData(action,*args):
    query = [str(action)]
    [query.append(str(x)) for x in args]
    return ";".join(query)

def separateCallbackData(data):
    """ Separate the callback data"""
    ret = []
    [ret.append(str(x)) for x in data.split(";")]
    if debug: print(ret)
    return ret

def valToBtn(val, callback = createCallbackData("IGNORE",0)):
    return InlineKeyboardButton(val, callback_data=callback)    

def langKeyboard(cancelText):
    langKeboardMarkup = InlineKeyboardMarkup([[
            valToBtn('🇩🇪 Deutsch', createCallbackData('LANG','de')),
            valToBtn('🇬🇧 English', createCallbackData('LANG','en')),
            valToBtn('🇵🇱 Polski', createCallbackData('LANG','pl'))],
        [
            valToBtn(cancelText, 'CANCEL')
        ]])
    return langKeboardMarkup