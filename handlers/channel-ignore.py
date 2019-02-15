#!/usr/bin/env python3
# encoding=utf-8

from telegram.ext import Filters, CommandHandler
import os
import functions.misc as misc
import pickle
import logging
import config

debug = config.debug

logger = logging.getLogger(__name__)

bannedFile = config.bannedFile
adminsFile = config.adminsFile

misc.bannedList = misc.loadFromFile(bannedFile)
adminsList = misc.loadFromFile(adminsFile)

if debug: print(misc.bannedList, adminsList)

def addAdmin(bot, update, args):
    if args != []:
        userId = int(args[0])
        adminsList.append(userId)
        misc.dumpToFile(adminsFile, adminsList)
        update.message.reply_text(
            f'Dodano usera o ID: {userId} do listy adminów.')

def rmAdmin(bot, update, args):
    if args != []:
        userId = int(args[0])
        adminsList.remove(userId)
        misc.dumpToFile(adminsFile, adminsList)
        update.message.reply_text(
            f'Usunięto usera o ID: {userId} z listy adminów.')

def ban(bot, update, args):
    user = update.message.from_user
    if not misc.isAdmin(user, adminsList):
        logger.info('user %s (%s) tried to ban someone', user.username, user.id)
        return
    if args != []:
        ban = str(args[0])
        misc.bannedList.append(ban)
        misc.dumpToFile(bannedFile, misc.bannedList)
        update.message.reply_text(
            f'Dodano usera o nicku/ID: {ban} do listy ignorowanych.')

def unban(bot, update, args):
    user = update.message.from_user
    if not misc.isAdmin(user, adminsList):
        logger.info('user %s (%s) tried to ban someone', user.username, user.id)
        return
    if args == []:
        update.message.reply_text('Nie podano ID/username.')
    elif str(args[0]) in misc.bannedList:
        misc.bannedList.remove(str(args[0]))
        update.message.reply_text(f'Usunięto {args[0]} z listy ignorowanych.')
        misc.dumpToFile(bannedFile, misc.bannedList)
    else:
        update.message.reply_text(f'Nie znaleziono {args[0]} na liście.')

def banlist(bot, update):
    user = update.message.from_user
    if not misc.isAdmin(user, adminsList):
        return
    text = 'Lista banów:'
    for user in misc.bannedList:
        text += '\n' + str(user)
    update.message.reply_text(text)

def help(bot, update):
    helpText = ('Lista komend:\n'
        '/ban [username/id] - blokuje autora wiadomości. Odpowiedz (reply) na sforwardowaną przez bota wiadomość a jej autor zostanie zbanowany.\n'
        '/unban [username/id] - odblokowuje użytkownika o podanym id/username.\n'
        '/banlist - wyświetla listę banów.')
    update.message.reply_text(helpText)


HANDLERS = (
    CommandHandler('addAdmin', addAdmin, pass_args=True, filters=
        (Filters.private & Filters.user(config.ownerID))),
    CommandHandler('rmAdmin', rmAdmin, pass_args=True, filters=
        (Filters.private & Filters.user(config.ownerID))),
    CommandHandler('ban', ban, pass_args=True, filters=Filters.private),
    CommandHandler('unban', unban, pass_args=True, filters=Filters.private),
    CommandHandler('banlist', banlist, filters=Filters.private),
    CommandHandler('help', help, filters=Filters.private),
)
