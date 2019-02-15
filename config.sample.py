#!/usr/bin/env python3
# encoding=utf-8

# API token
token = 'xxxxxx:xxxxxxxxxxxxx3ZoUdlMeuqHjAA'

# Channel / group ID 
# check message details in Plus Messenger - 'Group info' field.
# It needs to be prefixed by minus sign (-)
forwardDest = -36570000

# Report cooldown time (in minutes)
cooldown = 3

# Minimal message length
minMsgLen = 3

# Minimal alpha-num-space characters to emoji (and other non-alphanum chars) ratio for forwarded message
minCharRatio = 0.8

# Debug
debug = True

# Modules
# report - bot-to-channel/group forwarding module,
# group-ignore - user-ignore functionality, useful for 'helper' groups, all users on group can ban an user,
# channel-ignore - #TODO
modules = ['report', 'group-ignore']