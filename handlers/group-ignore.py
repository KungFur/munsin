#!/usr/bin/env python3
# encoding=utf-8

from telegram.ext import Filters, CommandHandler
import os
import functions.misc as misc
import pickle

bannedFile = 'banned'
bannedList = misc.loadFromFile(bannedFile)

def ban(bot, update, args):
    user = update.message.reply_to_message.forward_from
    if 'id' in args or user.username == None:
        ban = str(user.id)
    else:
        ban = user.username
    bannedList.append(ban)
    misc.dumpToFile(bannedFile, bannedList)
    update.message.reply_text(
        f'Dodano usera o nicku/ID: {ban} do listy ignorowanych.')


def unban(bot, update, args):
    if args == []:
        update.message.reply_text('Nie podano ID/username.')
    elif str(args[0]) in bannedList:
        bannedList.remove(str(args[0]))
        update.message.reply_text(f'Usunięto {args[0]} z listy ignorowanych.')
        misc.dumpToFile(bannedFile, bannedList)
    else:
        update.message.reply_text(f'Nie znaleziono {args[0]} na liście.')

def banlist(bot, update):
    text = 'Lista banów:'
    for user in bannedList:
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
    CommandHandler('ban', ban, pass_args=True, filters=Filters.group),
    CommandHandler('unban', unban, pass_args=True, filters=Filters.group),
    CommandHandler('banlist', banlist, filters=Filters.group),
    CommandHandler('help', help, filters=Filters.group),
)
