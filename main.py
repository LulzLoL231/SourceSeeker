#!env/bin/python3
# -*- coding: utf-8 -*-
# SourceSeeker – Main script
# Author: LulzLoL231
import asyncio
from time import sleep
from datetime import datetime

import discord

import config
import utils
import models


class SourceSeeker(discord.Client):
    def __init__(self):
        super().__init__()
        self.messages = {}
        self.servers = []
        self.InitServers()

    def InitServers(self):
        utils.log('InitServers', 'Initiating servers objects...')
        for i in config.servers:
            self.servers.append(models.Server.FromDict(i))
        utils.log('InitServers', f'Initiated {str(len(self.servers))} server\'s.')
        return True

    def IsMe(self, msg):
        return msg.author == bot.user

    async def SendServerInfo(self, server):
        if self.messages.keys().__contains__(server.server_name):
            for i in self.messages[server.server_name]:
                if server.refresh is True:
                    await i.edit(embed=server.GetEmbed())
                else:
                    await i.channel.send(embed=server.GetEmbed())
        else:
            self.messages[server.server_name] = []
            for chid in server.channels:
                ch = bot.get_channel(chid)
                self.messages[server.server_name].append(await ch.send(embed=server.GetEmbed()))

    async def Seek(self):
        utils.log('Seek', 'seeking...')
        while True:
            for i in self.servers:
                if i.IsMapChange():
                    i.UpdateInfo()
                    await self.SendServerInfo(i)
                elif i.IsPlayerCountChange():
                    if i.refresh:
                        i.UpdateInfo()
                        await self.SendServerInfo(i)
                    else:
                        pass
            await asyncio.sleep(5)

    async def PurgeMsgs(self):
        for serv in self.servers:
            for chid in serv.channels:
                ch = bot.get_channel(chid)
                if serv.refresh:
                    await ch.purge(limit=50, check=self.IsMe)
                    return True
                else:
                    await ch.purge(limit=1, check=self.IsMe)
                    return True

    async def on_ready(self):
        utils.log('SourceSeeker', f'Bot logged in as {str(bot.user)}')
        utils.log('on_ready', 'Purging messages...')
        await self.PurgeMsgs()
        utils.log('on_ready', 'Messages purged.')
        utils.log('on_ready', 'Sending Servers Info...')
        for i in self.servers:
            await self.SendServerInfo(i)
        await self.Seek()

    async def on_message(self, msg):
        if self.IsMe(msg):
            pass
        else:
            if msg.content.startswith(':'):
                utils.log('on_message', 'We have new message!')
                if msg.author == bot.get_user(config.admin):
                    utils.log('on_message', f'User: {str(msg.author)} [ADMIN] – {str(msg.content)}')
                    await msg.channel.send('Sorry ADMIN, i\'m temporary can\'t answer on an messages.')
                else:
                    utils.log('on_message', f'User: {str(msg.author)} – {str(msg.content)}')
                    await msg.channel.send('Sorry, i\'m temporary can\'t answer on an messages.')


if __name__ == '__main__':
    utils.log('SourceSeeker', 'Startup...')
    bot = SourceSeeker()
    bot.run(config.token)
