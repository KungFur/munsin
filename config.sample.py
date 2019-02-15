#!/usr/bin/env python3
# encoding=utf-8

# API token
token = 'xxxxxx:xxxxxxxxxxxxx3ZoUdlMeuqHjAA'

# Channel / group ID  (int)
# check message details in Plus Messenger - 'Group info' field.
# Needs to be provided as negative integer value. Channels prefix: -100
forwardDest = -36570000

# Report cooldown time (in minutes)
cooldown = 3

# Minimal message length
minMsgLen = 3

# Minimal alpha-num-space characters to emoji (and other non-alphanum chars) ratio for forwarded message
minCharRatio = 0.8

# Debug
debug = True

# Owner ID (int)
# Should be provided for channel-ignore module
ownerID = 0

# # Modules
# report - main bot-to-channel/group forwarding module,
#
# Select only one of the following modules
# group-ignore - user-ignore functionality, useful for 'helper' groups, all users on group can ban an user,
# channel-ignore - banning users directly from bot commands (owner can add admins)
modules = ['report', 'group-ignore']

# # Files
bannedFile = 'banned' # filename for storing banned users
adminsFile = 'admins' # filename for storing admins