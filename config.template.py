# -*- coding: utf-8 -*-
# SourceSeeker – config
# Author: LulzLoL231
import logging


debug         = False         # SourceSeeker Debug mode.
logging_level = logging.INFO  # Logger level.

###   APPEND HERE YOUR Discord CREDENTIALS    ###
#
#     Setup like: token = DISCORD_TOKEN
#
#     DISCORD_TOKEN – Your discord bot token
#     admin         – Admin Discord UserID
#
token = 'DISCORD_TOKEN'
admin = 0


###   APPEND HERE YOUR Source SERVER   ####
#
#     Setup like: {'addr': address, 'channels': channels, 'inline': inline, 'refresh': refresh, 'memo': memo}
#
#     address    – server_ip and server_port in tuple.
#     channels   – Discord channels IDs.
#     inline     – Embed view inline or not, boolean.
#     refresh    – Select map change response mode, "True" – just edit msg; False – send new message always after change map.
#     memo       – Server name. (optional)
#
servers = [

]
