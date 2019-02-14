#!/usr/bin/env python3
# encoding=utf-8

# ################
# ##
# ## Forwarding Bot for Telegram
# ## 

import telegram.bot
from telegram.ext import messagequeue as mq
import config
import logging
from datetime import datetime, timedelta

debug = config.debug

logger = logging.getLogger(__name__)

def error(bot, update, err):
    """Log all errors"""
    logger.warning(f'Update "{update}" caused error "{err}"')


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


if __name__ == '__main__':
    from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import MessageHandler, Filters, ConversationHandler, CommandHandler, RegexHandler, CallbackQueryHandler
    from telegram.utils.request import Request
    import os
    from text import text
    import misc

    token = config.token
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot 
    request = Request(con_pool_size=8)
    testbot = MQBot(token, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=testbot)

    def start(bot, update, user_data):
        if debug: print(user_data)
       
        if 'lang' not in user_data:
            userLang = update.message.from_user.language_code
            if userLang not in ['pl', 'de']:
                user_data['lang'] = 'en'
            else:
                user_data['lang'] = userLang

        if 'lastUsed' in user_data:
            cooldown = (user_data['lastUsed'] - datetime.now() + timedelta(minutes = config.cooldown)).total_seconds()

            if cooldown > 0:
                update.message.reply_text(text('cooldown_' + user_data['lang'], round(cooldown)))
                return ConversationHandler.END

        update.message.reply_text(text('start_' + user_data['lang']),
            reply_markup = misc.langKeyboard(user_data['lang']))
        return GET_REPORT

    def startHandler(bot, update, user_data):
        query = update.callback_query
        data = misc.separateCallbackData(query.data)

        action = data.pop(0)

        if action == 'LANG':
            user_data['lang'] = data[0]
            try:
                bot.edit_message_text(chat_id = query.message.chat_id, 
                    message_id = query.message.message_id,
                    text = text('start_' + user_data['lang']),
                    reply_markup = misc.langKeyboard(user_data['lang']))
            except:
                bot.answer_callback_query(callback_query_id= query.id)  
        elif action == 'CANCEL':
            try:
                bot.edit_message_text(chat_id = query.message.chat_id, 
                    message_id = query.message.message_id,
                    text = text('cancelled_' + user_data['lang']))
            except:
                pass        
            return ConversationHandler.END

    def forwardMsg(bot, update, user_data):

        if debug: print(update.message)
           
        alnumCount = 0
        for char in update.message.text:
            if char.isalnum(): alnumCount += 1
            elif char.isspace(): alnumCount += 1
        
        if len(update.message.text) < config.minMsgLen or alnumCount < 0.8 * len(update.message.text):
            update.message.reply_text(text('msgTooShort_' + user_data['lang']))
            return

        bot.forward_message(chat_id = config.forwardDest,
            from_chat_id = update.message.chat.id,
            message_id = update.message.message_id
            )

        update.message.reply_text(text('end_' + user_data['lang']))

        user_data['lastUsed'] = datetime.now()

        return ConversationHandler.END
        
    def cancel(bot, update, user_data):
        update.message.reply_text(text('cancelled_' + user_data['lang']), reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END



    GET_REPORT = range(1)

    reportAction = ConversationHandler(
        entry_points= [(CommandHandler('start', start, pass_user_data=True, filters= ~Filters.group))],

        states={
            GET_REPORT: [CallbackQueryHandler(startHandler, pass_user_data=True),
            MessageHandler(Filters.text, forwardMsg, pass_user_data=True)]
        },

        fallbacks=[CommandHandler(
            'cancel', cancel, pass_user_data=True)]
    
    )

    upd.dispatcher.add_handler(reportAction)

    upd.dispatcher.add_error_handler(error)
    upd.start_polling()