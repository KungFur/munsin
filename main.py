#!/usr/bin/env python3
# encoding=utf-8

import telegram.bot
from telegram.ext import messagequeue as mq
import config
import logging

debug = config.debug

logging.basicConfig(format='[%(asctime)s][%(name)s] %(message)s', level=logging.INFO)
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
    import os
    import importlib

    token = config.token
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot 
    request = Request(con_pool_size=8)
    testbot = MQBot(token, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=testbot)

    for module in config.modules:
        handlers = getattr(importlib.import_module(f'handlers.{module}'), 'HANDLERS')
        logger.info('module imported: %s (handlers: %d)', module, len(handlers))
        for handler in handlers:
            upd.dispatcher.add_handler(handler)

    upd.dispatcher.add_error_handler(error)
    upd.start_polling()