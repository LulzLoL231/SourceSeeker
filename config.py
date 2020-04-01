# -*- coding: utf-8 -*-
# SourceSeeker – config
# Author: LulzLoL231

###   APPEND HERE YOUR Discord CREDENTIALS    ###
#
#     Setup like: token = DISCORD_TOKEN
#
#     DISCORD_TOKEN – Your discord bot token
#
token = 'NjgyMjY2NDYxODA0NDI5NDI2.XoEn5w.jWT7I2WthhDeICKmjF7HB-obPu4'


###   APPEND HERE YOUR Discord Channels IDs   ###
#
#     Setup like: 'CHANNEL_NAME': CHANNEL_ID
#
#     CHANNEL_NAME – Discord channel name
#     CHANNEL_ID   – Discord channel id
#
channels = {
    'lesnik': 692819106583412766
}


###   APPEND HERE YOUR Source SERVER   ####
#
#     Setup like: Server(address, channels, inline, refresh)
#
#     address    – server_ip and server_port in tuple
#     channels   – Discord channels IDs, from "channels" var.
#     inline     – Embed view inline or not, boolean.
#     refresh – Select map change response mode, "True" – just edit msg; False – send new message always after change map.
#
servers = [
    #Server(('68.183.113.119', 27015), [channels['seeker']], False, True),  # LulzCS
    #Server(('89.163.189.122', 27015), [channels['seeker']], True, True),  # Miza2
    #Server(('195.80.138.162', 27015), [channels['seeker']], True, True),  # Miza4
    Server(('46.174.55.249', 27015), [channels['lesnik']], False, False)  # Lesnik ZM Server
]
