#!/usr/bin/env python3
# encoding=utf-8

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import debug, ownerID
import pickle
import os

bannedList = []

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

def loadFromFile(file):
    if os.path.getsize(file) > 0:
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def dumpToFile(file, data):
    with open(file, 'wb') as f:
            pickle.dump(data, f)

def isAdmin(user, adminsList):
    if user.id in adminsList or user.id == ownerID:
        return True
    else:
        return False