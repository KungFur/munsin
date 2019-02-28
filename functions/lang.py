#!/usr/bin/env python3
# encoding=utf-8

import logging
logger = logging.getLogger(__name__)

def validator(lang):
    error = False

    if "langKeyboard" not in lang:
        logger.error("Error: No 'langKeyboard' object")
        
        raise ValueError ("Error: No 'langKeyboard' object")
    
    if set(['buttons', 'cancel']) > set(lang["langKeyboard"].keys()):
        logger.error("Error: Wrong 'langKeyboard' configuration (no buttons or cancel objects)")
        raise ValueError ("Error:  Wrong 'langKeyboard' configuration (no buttons or cancel objects)")
    
    langs = lang["langKeyboard"]["buttons"].keys()
    logger.info(f"LangValidator: Detected {langs} in json file, testing all messages.")

    for msg in lang.keys():
        if msg != "langKeyboard":
            for langCode in langs:
                if lang[msg].get(langCode, None) == None:
                    logger.error(f"Error: *{msg}* has no value for *{langCode}* code.")
                    error = True
    
    if error:
        raise ValueError

    logger.info("LangValidator: Test completed, all seems to be OK")

    del lang



