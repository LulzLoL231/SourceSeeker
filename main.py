#!/env/bin python3
# -*- coding: utf-8 -*-
# SourceSeeker – Main script
# Author: LulzLoL231
import asyncio
from time import sleep
from datetime import datetime

import discord

from config import *


class SourceSeeker(discord.Client):
    def __init__(self):
        super().__init__()
        self.messages = {}

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
        for i in servers:
            if i.IsMapChange():
                i.UpdateInfo()
                await self.SendServerInfo(i)
            elif i.IsPlayerCountChange():
                if i.refresh:
                    i.UpdateInfo()
                    await self.SendServerInfo(i)
                else:
                    pass

    async def PurgeMsgs(self):
        for serv in servers:
            for chid in serv.channels:
                ch = bot.get_channel(chid)
                if serv.refresh:
                    await ch.purge(limit=200, check=self.IsMe)
                else:
                    await ch.purge(limit=1, check=self.IsMe)

    async def on_ready(self):
        await self.PurgeMsgs()
        for i in servers:
            await self.SendServerInfo(i)
        while True:
            await self.Seek()
            sleep(5)

if __name__ == '__main__':
    bot = SourceSeeker()
    bot.run(token)
