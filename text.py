#!/usr/bin/env python3
# encoding=utf-8

def text(id, *arg):

    ## Start message
    if id == 'start_en':
        ret = 'Start msg in ENG'
    
    elif id == 'start_pl':
        ret = 'Start msg in PL'

    elif id == 'start_de':
        ret = 'Start msg in DE'

    ## End message
    
    elif id == 'end_pl':
        ret = 'End msg in PL. Type /start to restart.'

    elif id == 'end_de':
        ret = 'End msg in DE. Type /start to restart.'

    elif id == 'end_en':
        ret = 'End msg in EN. Type /start to restart.'

    ## Cancelled message

    elif id == 'cancelled_pl':
        ret = 'Cancelled msg in PL. Type /start to restart.'

    elif id == 'cancelled_de':
        ret = 'Cancelled msg in DE. Type /start to restart.'

    elif id == 'cancelled_en':
        ret = 'Cancelled msg in EN. Type /start to restart.'

    ## Cooldown message

    elif id == 'cooldown_pl':
        ret = f'Poczekaj {arg[0]} sek. zanim wyślesz kolejną wiadomość. Po tym czasie wyślij /start by zacząć ponownie.'

    elif id == 'cooldown_de':
        ret = f'Bitte warten {arg[0]} sek, bevor weitere Nachrichten senden. Nach dem Warten senden /start um es erneut zu versuchen.'

    elif id == 'cooldown_en':
        ret = f'Please wait {arg[0]} sec before submitting another message. After waiting, send /start to try again.'

    ## Message too short

    elif id == 'msgTooShort_pl':
        ret = f'Msg too short in PL.'

    elif id == 'msgTooShort_de':
        ret = f'Msg too short in DE.'

    elif id == 'msgTooShort_en':
        ret = f'Msg too short in EN.'

    
    ## Cancel button

    elif id == 'canc_pl':
        ret = 'Anuluj'

    elif id == 'canc_de':
        ret = 'Cancel (DE)'

    elif id == 'canc_en':
        ret = 'Cancel'

    



    ## ID error
    else:
        ret = 'Wrong ID'
        print('id: ', id)
        print('args:', arg)

    return ret