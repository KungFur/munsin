#!/usr/bin/env python3
# encoding=utf-8

from telegram.ext import Filters, CommandHandler
import os
import functions.misc as misc
import pickle
import config

bannedFile = config.bannedFile
misc.bannedList = misc.loadFromFile(bannedFile)

def ban(bot, update, args):
    user = update.message.reply_to_message.forward_from
    if 'id' in args or user.username == None:
        ban = str(user.id)
    else:
        ban = user.username
    misc.bannedList.append(ban)
    misc.dumpToFile(bannedFile, misc.bannedList)
    update.message.reply_text(
        f'Dodano usera o nicku/ID: {ban} do listy ignorowanych.')

def unban(bot, update, args):
    if update.message.reply_to_message != None:
        user = update.message.reply_to_message.forward_from
        if str(user.id) in misc.bannedList:
            unban = str(user.id)
        elif user.username != None and user.username in misc.bannedList:
            unban = user.username
        else:
            update.message.reply_text('Autor wiadomości nie jest na liście ignorowanych.')
            return
    elif args == []:
        update.message.reply_text('Nie podano ID/username.')
        return
    elif str(args[0]) in misc.bannedList:
        unban = str(args[0])
    else:
        update.message.reply_text(f'Nie znaleziono {args[0]} na liście.')
        return
    misc.bannedList.remove(unban)
    misc.dumpToFile(bannedFile, misc.bannedList)
    update.message.reply_text(f'Usunięto użytkownika/ID: {unban} z listy ignorowanych.')

def banlist(bot, update):
    text = 'Lista banów:'
    for user in misc.bannedList:
        text += '\n' + str(user)
    update.message.reply_text(text)

def help(bot, update):
    helpText = ('Lista komend:\n'
        '/ban - blokuje autora wiadomości. Odpowiedz (reply) na sforwardowaną przez bota wiadomość a jej autor zostanie zbanowany.\n'
        '/ban id - jak wyżej, blokuje ID (przydatne gdy ktoś zmienia username).\n'
        '/unban [username/id] - odblokowuje użytkownika o podanym id/username.\n'
        '/banlist - wyświetla listę banów.')
    update.message.reply_text(helpText)


HANDLERS = (
    CommandHandler('ban', ban, pass_args=True, 
        filters=(Filters.group & Filters.reply)),
    CommandHandler('unban', unban, pass_args=True, filters=Filters.group),
    CommandHandler('banlist', banlist, filters=Filters.group),
    CommandHandler('help', help, filters=Filters.group),
)
