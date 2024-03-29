#!/usr/bin/env python3
# encoding=utf-8

import telegram.bot
from telegram.ext import messagequeue as mq
import config
import logging
import sys

def get_log_level():
    log_level = "INFO"
    try:
        log_level = config.log_level
    except:
        print("Log level not declared. Defaulting to INFO")
    return getattr(logging,log_level)

def get_log_file_path():
    log_file = "main.log"
    try:
        log_file = config.log_file
    except:
        print('Log file not declared. Defaulting to "main.log"')
    return log_file

def get_log_output():
    log_output = "stdout"
    try:
        log_output = config.log_output
    except:
        print("Log output not declared. Defaulting to standard output.")
    return log_output

debug = config.debug
log_level = get_log_level()
log_output = get_log_output()

if log_output == "stdout":
    logging.basicConfig(stream=sys.stdout, format='[%(name)s] %(message)s', level=log_level)
if log_output == "file":
    logging.basicConfig(filename=get_log_file_path(), format='[%(asctime)s][%(name)s] %(message)s', 
        level=log_level)

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
    from telegram.utils.request import Request
    from telegram.ext import Filters, CommandHandler
    import os
    import sys
    import importlib

    from threading import Thread

    token = config.token
    # set message queue limits: 20msgs/60s for groups or 30msgs/s for user chats
    q = mq.MessageQueue(all_burst_limit=19, all_time_limit_ms=60000)
    # set connection pool size for bot 
    request = Request(con_pool_size=8)
    tgBot = MQBot(token, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=tgBot)

    for module in config.modules:
        handlers = getattr(importlib.import_module(f'handlers.{module}'), 'HANDLERS')
        logger.info('module imported: %s (handlers: %d)', module, len(handlers))
        for handler in handlers:
            upd.dispatcher.add_handler(handler)

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        upd.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def stop():
        upd.stop()

    def restart(bot, update):
        update.message.reply_text('Bot is restarting...')
        logger.info('Bot is restaring...')
        Thread(target=stop_and_restart).start()

    upd.dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(user_id=config.ownerID)))
    upd.dispatcher.add_error_handler(error)
    upd.start_polling()
    upd.idle()
