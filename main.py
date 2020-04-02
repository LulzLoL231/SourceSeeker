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

    async def InitServers(self):
        utils.log('InitServers', 'Initiating servers objects...')
        for i in config.servers:
            self.servers.append(models.Server.FromDict(i))
        utils.log('InitServers', f'Initiated {str(len(self.servers))} server\'s.')
        return True

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
                if await i.IsMapChange():
                    await i.UpdateInfo()
                    await self.SendServerInfo(i)
                elif await i.IsPlayerCountChange():
                    if i.refresh:
                        await i.UpdateInfo()
                        await self.SendServerInfo(i)
                    else:
                        pass
            await asyncio.sleep(5)

    async def PurgeMsgs(self):
        for serv in self.servers:
            for chid in serv.channels:
                ch = bot.get_channel(chid)
                if serv.refresh:
                    await ch.purge(limit=50, check=Commands.IsMe)
                    return True
                else:
                    await ch.purge(limit=1, check=Commands.IsMe)
                    return True

    async def init(self):
        self.messages = {}
        utils.log('on_ready', 'Purging messages...')
        await self.PurgeMsgs()
        utils.log('on_ready', 'Messages purged.')
        utils.log('on_ready', 'Sending Servers Info...')
        for i in self.servers:
            await self.SendServerInfo(i)
        await self.Seek()

    async def on_ready(self):
        await self.InitServers()
        utils.log('SourceSeeker', f'Bot logged in as {str(bot.user)}')
        await self.init()

    async def on_message(self, msg):
        await Commands.recognize(msg)


class Commands:
    cmds = ['help', 'admin.reload', 'admin.purge']
    def IsMe(msg):
        return msg.author == bot.user

    def IsCmd(msg):
        return msg.content.startswith(':')

    def IsCmdOrMe(msg):
        return Commands.IsCmd(msg) or Commands.IsMe(msg)

    async def recognize(msg):
        if Commands.IsMe(msg):
            pass
        else:
            if Commands.IsCmd(msg):
                utils.log('Commands.recognize', f'Recieved command: {msg.content}; From: {str(msg.author)}')
                if msg.content.strip(':') in Commands.cmds:
                    utils.log('Commands.recognize', 'Recieved command is valid. Executing.')
                    cmd = eval(f'Commands.{msg.content.strip(":")}')
                    await cmd(msg)
                else:
                    utils.log('Commands.recognize', 'Recieved command is not valid.')
                    await Commands.NotValid(msg)
            else:
                if msg.channel.guild:
                    # Its not DM msg.
                    utils.log('Commands.recognize', f'Recieved channel message. Ignoring.')
                else:
                    # DM msg.
                    utils.log('Commands.recognize', f'Recieved message: {msg.content}; From: {str(msg.author)}')
                    await Commands.Sorry(msg)

    async def NotValid(msg):
        await msg.channel.send('Sorry, this command is not valid, enter `:help` for get all available commands.')
        await asyncio.sleep(3)
        await msg.channel.purge(limit=1, check=Commands.IsCmdOrMe)

    async def Sorry(msg):
        await msg.channel.send('Sorry, i don\'t understand you.')
        await asyncio.sleep(3)
        await msg.channel.purge(limit=1, check=Commands.IsCmdOrMe)

    async def help(msg):
        cnt = 'Available commands:\n`:help`: get you this msg.\n`:info`: get bot info.'
        await msg.channel.send(cnt)

    async def ok(msg):
        await msg.channel.send('Complete.')
        await asyncio.sleep(3)
        await msg.channel.purge(limit=1, check=Commands.IsCmdOrMe)

    async def denied(msg):
        await msg.channel.send('Access Denied.')
        await asyncio.sleep(3)
        await msg.channel.purge(limit=1, check=Commands.IsCmdOrMe)

    class admin:
        def IsAdmin(msg):
            return msg.author == bot.get_user(config.admin)

        async def reload(msg):
            if Commands.admin.IsAdmin(msg):
                utils.log('Commands.admin.reload', f'Called admin cmd "reload" from user: {str(msg.author)}. Access Granted.')
                await bot.init()
                await Commands.ok(msg)
            else:
                utils.log('Commands.admin.reload', f'Called admin cmd "reload" from user: {str(msg.author)}. Access Denied.', 'warn')
                await Commands.denied(msg)

        async def purge(msg):
            if Commands.admin.IsAdmin(msg):
                utils.log('Commands.admin.purge', f'Called admin cmd "purge" from user: {str(msg.author)}. Access Granted.')
                await msg.channel.purge(limit=100, check=Commands.IsCmdOrMe)
                await bot.init()
                await Commands.ok(msg)
            else:
                utils.log('Commands.admin.purge', f'Called admin cmd "purge" from user: {str(msg.author)}. Access Denied.', 'warn')
                await Commands.denied(msg)



#async def start():
#    global bot
if __name__ == '__main__':
    utils.log('SourceSeeker', '--- STARTUP ---')
    bot = SourceSeeker()
    bot.run(config.token)

#asyncio.run(start())
