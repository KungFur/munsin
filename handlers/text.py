#!/usr/bin/env python3
# encoding=utf-8

def text(id, *arg):

    ## Start message
    if id == 'start_en':
        ret = ("Hi, I'm a Telegram Bot for contacting Gdakon ConOps. If you have any problems or questions, I will forward them to ConOps, so they can get back to you / help you.\n\n"
            "Please enter your message below:")
    
    elif id == 'start_pl':
        ret = ('Cześć, jestem telegramowym botem który pomoże Ci skontaktować się z Gdakonową ekipą (ConOps). Jeśli masz  jakiś problem, pytanie, bądź potrzebujesz pomocy - przekażę im Twoją wiadomość. Jeśli możesz, proszę pisz w języku angielskim.\n\n'
            'Wpisz swoją wiadomość poniżej:')

    elif id == 'start_de':
        ret = ("Hallo, Ich bin ein Telegram Bot, der Dir hilft, bei Fragen und Problemen mit jemandem vom ConOps in Kontakt zu treten. Wenn du kannst, schreib bitte auf Englisch.\n\n"
            "Bitte geben Deine Nachricht unten:")

    ## End message
    
    elif id == 'end_pl':
        ret = ('Twoje zgłoszenie zostało przekazane Gdakonowej ekipie. Skontaktujemy się z Tobą jeśli będzie taka potrzeba.\n'
             'Wpisz /start aby rozpocząć ponownie.')

    elif id == 'end_de':
        ret = ' Deine Nachricht wurde an das Gdakon Team weitergeleitet. Wir werden uns, falls nötig, bei dir melden.'

    elif id == 'end_en':
        ret = ("Your message has been forwarded to the Gdakon team. We'll contact you if neccessary.\n"
            'Use /start command if you want to send another message.')

    ## Cancelled message

    elif id == 'cancelled_pl':
        ret = 'Anulowano. Wpisz /start by rozpocząć ponownie.'

    elif id == 'cancelled_de':
        ret = 'Abgebrochen. Type /start to restart.'

    elif id == 'cancelled_en':
        ret = 'Cancelled. Send /start to retry.'

    ## Cooldown message

    elif id == 'cooldown_pl':
        ret = f'Poczekaj {arg[0]} sek. zanim wyślesz kolejną wiadomość. Po tym czasie wyślij /start by zacząć ponownie.'

    elif id == 'cooldown_de':
        ret = f'Bitte warten {arg[0]} sek, bevor weitere Nachrichten senden. Nach dem Warten senden /start um es erneut zu versuchen.'

    elif id == 'cooldown_en':
        ret = f'Please wait {arg[0]} sec before submitting another message. After waiting, send /start to try again.'

    ## Message too short

    elif id == 'msgTooShort_pl':
        ret = 'Wiadomość za krótka.'

    elif id == 'msgTooShort_de':
        ret = 'Nachricht zu kurz.'

    elif id == 'msgTooShort_en':
        ret = 'Message is too short'

    ## User banned

    elif id == 'banned_pl':
        ret = 'Zostałeś zablokowany.'

    elif id == 'banned_de':
        ret = 'You have been blocked.'

    elif id == 'banned_en':
        ret = 'You have been blocked.'

    
    ## Cancel button

    elif id == 'canc_pl':
        ret = 'Anuluj'

    elif id == 'canc_de':
        ret = 'Abbrechen'

    elif id == 'canc_en':
        ret = 'Cancel'

    



    ## ID error
    else:
        ret = 'Wrong ID'
        print('id: ', id)
        print('args:', arg)

    return ret