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
import functions.lang as lang
import logging

logger = logging.getLogger(__name__)

text = json.load(open('lang.json', encoding='utf8'))
lang.validator(text)

def start(bot, update, user_data):
    user = update.message.from_user
    logger.debug('user_data: %s', user_data)
    logger.debug('bannedList: %s', misc.bannedList)
    logger.debug('user: %s', user)

    if user.username in misc.bannedList or str(user.id) in misc.bannedList:
        update.message.reply_text(text['banned']['pl'])
        return ConversationHandler.END

    if 'lastUsed' in user_data:
        cooldown = (user_data['lastUsed'] - datetime.now() +
                    timedelta(minutes=config.cooldown)).total_seconds()

        if cooldown > 0:
            update.message.reply_text(text['cooldown']['pl'] %round(cooldown))
            return ConversationHandler.END

    update.message.reply_text(text['start']['pl'])
    return GET_REPORT


def startHandler(bot, update, user_data):
    query = update.callback_query
    data = misc.separateCallbackData(query.data)

    action = data.pop(0)

    if action == 'LANG':
        user_data['lang'] = 'pl'
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text['start']['pl'])
        except:
            bot.answer_callback_query(callback_query_id=query.id)
    elif action == 'CANCEL':
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text['start']['pl'])
        except:
            pass
        return ConversationHandler.END


def forwardMsg(bot, update, user_data):

    logger.debug('received message: %s', update.message)

    alnumCount = 0
    for char in update.message.text:
        if char.isalnum():
            alnumCount += 1
        elif char.isspace():
            alnumCount += 1

    if len(update.message.text) < config.minMsgLen or alnumCount < config.minCharRatio * len(update.message.text):
        update.message.reply_text(text['msgTooShort']['pl'])
        return

    bot.forward_message(chat_id=config.forwardDest,
                        from_chat_id=update.message.chat.id,
                        message_id=update.message.message_id,
                        disable_notification=config.silent
                        )

    bot.send_message(chat_id=config.forwardDest,
                     text=update.message.from_user.full_name+' ('+update.message.from_user.name+')')

    update.message.reply_text(text['end']['pl'])

    user_data['lastUsed'] = datetime.now()

    return ConversationHandler.END


def cancel(bot, update, user_data):
    update.message.reply_text(
        text['cancelled']['pl'], reply_markup=ReplyKeyboardRemove())
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
