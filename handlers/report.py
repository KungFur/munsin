#!/usr/bin/env python3
# encoding=utf-8

from telegram import ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters, ConversationHandler, CommandHandler, RegexHandler, CallbackQueryHandler
from telegram.utils.request import Request
import os
import functions.misc as misc
import pickle
import config
from datetime import datetime, timedelta
import json

debug = config.debug

print('report')

text = json.load(open('lang.json', encoding='utf8'))

def start(bot, update, user_data):
    if debug:
        print(user_data)
        print(misc.bannedList)
    user = update.message.from_user

    if 'lang' not in user_data:
        userLang = user.language_code
        if userLang not in text['langKeyboard']['buttons'].keys():
            user_data['lang'] = 'en'
        else:
            user_data['lang'] = userLang

    if user.username in misc.bannedList or str(user.id) in misc.bannedList:
        update.message.reply_text(text['banned'][user_data['lang']])
        return ConversationHandler.END

    if 'lastUsed' in user_data:
        cooldown = (user_data['lastUsed'] - datetime.now() +
                    timedelta(minutes=config.cooldown)).total_seconds()

        if cooldown > 0:
            update.message.reply_text(text['cooldown'][user_data['lang']] %round(cooldown))
            return ConversationHandler.END

    update.message.reply_text(text['start'][user_data['lang']],
                              reply_markup=misc.langKeyboard(text['langKeyboard'],user_data['lang']))
    return GET_REPORT


def startHandler(bot, update, user_data):
    query = update.callback_query
    data = misc.separateCallbackData(query.data)

    action = data.pop(0)

    if action == 'LANG':
        user_data['lang'] = data[0]
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text['start'][user_data['lang']],
                                  reply_markup=misc.langKeyboard(text['langKeyboard'],user_data['lang']))
        except:
            bot.answer_callback_query(callback_query_id=query.id)
    elif action == 'CANCEL':
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text['cancelled'][user_data['lang']])
        except:
            pass
        return ConversationHandler.END


def forwardMsg(bot, update, user_data):

    if debug:
        print(update.message)

    alnumCount = 0
    for char in update.message.text:
        if char.isalnum():
            alnumCount += 1
        elif char.isspace():
            alnumCount += 1

    if len(update.message.text) < config.minMsgLen or alnumCount < config.minCharRatio * len(update.message.text):
        update.message.reply_text(text['msgTooShort'][user_data['lang']])
        return

    bot.forward_message(chat_id=config.forwardDest,
                        from_chat_id=update.message.chat.id,
                        message_id=update.message.message_id
                        )

    update.message.reply_text(text['end'][user_data['lang']])

    user_data['lastUsed'] = datetime.now()

    return ConversationHandler.END


def cancel(bot, update, user_data):
    update.message.reply_text(
        text['cancelled'][user_data['lang']], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


GET_REPORT = range(1)

HANDLERS = (
    ConversationHandler(
        entry_points=[
            (CommandHandler('start', start, pass_user_data=True, filters=~Filters.group))],

        states={
            GET_REPORT: [CallbackQueryHandler(startHandler, pass_user_data=True),
                         MessageHandler(Filters.text, forwardMsg, pass_user_data=True)]
        },

        fallbacks=[CommandHandler(
            'cancel', cancel, pass_user_data=True)]

    ),
)
