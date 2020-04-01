# -*- coding: utf-8 -*-
# SourceSeeker – config
# Author: LulzLoL231
import logging
debug         = True          # SourceSeeker Debug mode.
logging_level = logging.INFO  # Logger level.

###   APPEND HERE YOUR Discord CREDENTIALS    ###
#
#     Setup like: token = DISCORD_TOKEN
#
#     DISCORD_TOKEN – Your discord bot token
#
token = 'NjgyMjY2NDYxODA0NDI5NDI2.XoRAxA.7BbRNaE0-BA9dOCNstpEQndXaVw'  # LzTestBot
admin = 399493754517454848


###   APPEND HERE YOUR Source SERVER   ####
#
#     Setup like: Server(address, channels, inline, refresh)
#
#     address    – server_ip and server_port in tuple
#     channels   – Discord channels IDs, from "channels" var.
#     inline     – Embed view inline or not, boolean.
#     refresh    – Select map change response mode, "True" – just edit msg; False – send new message always after change map.
#     memo       – Server name. (optional)
#
servers = [
    {
        'addr': ('68.183.113.119', 27015),
        'channels': [692431677854580797],
        'inline': True,
        'refresh': True,
        'memo': 'LulzCS'
    },
    {
        'addr': ('195.80.138.162', 27015),
        'channels': [692431677854580797],
        'inline': True,
        'refresh': True,
        'memo': 'Mizapro ZE #4'
    }
    #Server(('68.183.113.119', 27015), [channels['seeker']], False, True),  # LulzCS
    #Server(('89.163.189.122', 27015), [channels['seeker']], True, True),  # Miza2
    #Server(('195.80.138.162', 27015), [channels['seeker']], True, True),  # Miza4
    #Server(('46.174.55.249', 27015), [channels['lesnik']], False, False)  # Lesnik ZM Server
]
