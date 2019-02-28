#!/usr/bin/env python3
# encoding=utf-8

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import ownerID
import pickle
import os
import logging

logger = logging.getLogger(__name__)

bannedList = []

def createCallbackData(action,*args):
    query = [str(action)]
    [query.append(str(x)) for x in args]
    return ";".join(query)

def separateCallbackData(data):
    """ Separate the callback data"""
    ret = []
    [ret.append(str(x)) for x in data.split(";")]
    logger.debug('separated callback data: %s', ret)
    return ret

def valToBtn(val, callback = createCallbackData("IGNORE",0)):
    return InlineKeyboardButton(val, callback_data=callback)    

def langKeyboard(langKeyDict, langCode):
    langKeyboardMarkup = [[],[]]
    for code, label in langKeyDict['buttons'].items():
        langKeyboardMarkup[0].append(
            valToBtn(label, createCallbackData('LANG',code)))
    langKeyboardMarkup[1].append(
        valToBtn(langKeyDict['cancel'][langCode], 'CANCEL')
    )
    return InlineKeyboardMarkup(langKeyboardMarkup)

def loadFromFile(file):
    if os.path.exists(file) == False:
        open(file, 'a')
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