# -*- coding: utf-8 -*-
# SourceSeeker – models
# Author: LulzLoL231
import os
from datetime import datetime

import a2s
from discord import Embed, Colour


def log(message, type):
    if os.path.isfile('SourceSeeker.log'):
        if os.path.getsize('SourceSeeker.log') >= 1073741824:
            os.remove('SourceSeeker.log')
    with open('SourceSeeker.log', 'w') as file:
        file.write(f'[ {str(datetime.now())} ] // ( {type} ) – {message}')
        file.close()


def GetServerInfo(addr):
    recv = False
    iter = 0
    while recv != True:
        try:
            i = a2s.info(addr)
        except Exception as e:
            log(f'func "GetServerInfo": Address [{str(addr)}] – {e}')
            if iter <= 5:
                return None
            else:
                iter += 1
                continue
        else:
            recv = True
            return i


def GetFastConnectURI(addr):
    return f'steam://connect/{addr[0]}:{addr[1]}'


def GetEmbedDict(server=None, SteamURI=None, inline=False, offline=False):
    embed_wo_inline = {
                    'title': '',
                    'description': '',
                    'color': None,
                    'timestamp': '',
                    'footer':{'icon_url':'https://cdn.discordapp.com/avatars/692377987349217363/19c8c19cabaebaf106be1e78c065aa2d.webp','text': 'SourceSeeker by LulzLoL231#9006'}}
    embed_inline = {
                    'title': '',
                    'color': None,
                    'timestamp': '',
                    'footer':{'icon_url':'https://cdn.discordapp.com/avatars/692377987349217363/19c8c19cabaebaf106be1e78c065aa2d.webp','text': 'SourceSeeker by LulzLoL231#9006'},'fields':[{'name': 'Map','value': '','inline':True},{'name': 'Player Count','value': '','inline': True},{'name': 'Fast Connect','value': '','inline':True}]}
    if inline is True:
        embed = embed_inline.copy()
        embed['timestamp'] = datetime.isoformat(datetime.now())
        if offline:
            embed['title'] = offline
            embed['description'] = '**Offline or Unavailable.**'
            embed['color'] = Colour.red().value
        else:
            embed['title'] = server.server_name
            embed['color'] = Colour.green().value
        embed['fields'][0]['value'] = '**'+server.map_name+'**'
        embed['fields'][1]['value'] = '**'+str(server.player_count)+'**'
        embed['fields'][2]['value'] = '**'+SteamURI+'**'
    else:
        embed = embed_wo_inline.copy()
        embed['timestamp'] = datetime.isoformat(datetime.now())
        if offline:
            embed['title'] = offline
            embed['description'] = '**Offline or Unavailable.**'
            embed['color'] = Colour.red().value
        else:
            embed['title'] = server.server_name
            embed['color'] = Colour.green().value
            embed['description'] = 'Current map: **{}**\nPlayers online: **{}**\nFast connect: **{}**'.format(server.map_name, server.player_count, SteamURI)
    return embed


class Server:
    def __init__(self, address, channels, inline, refresh):
        self.address = address
        self.info = GetServerInfo(address)
        if self.info is None:
            self.server_name = 'Unknown Source Server'
        else:
            self.server_name = self.info.server_name
        self.SteamURI = GetFastConnectURI(address)
        self.channels = channels
        self.inline = inline
        self.refresh = refresh

    def GetEmbed(self):
        if self.info is None:
            return Embed.from_dict(GetEmbedDict(offline=self.server_name, SteamURI=self.SteamURI))
        return Embed.from_dict(GetEmbedDict(self.info, self.SteamURI, self.inline))

    def IsMapChange(self):
        seek = GetServerInfo(self.address)
        if (seek is None) or (self.info is None):
            return True
        elif seek.map_name != self.info.map_name:
            return True
        else:
            return False

    def UpdateInfo(self):
        self.info = GetServerInfo(self.address)
        return True

    def GetMap(self):
        return self.info.map_name

    def IsPlayerCountChange(self):
        seek = GetServerInfo(self.address)
        if (seek is None) or (self.info is None):
            return True
        elif seek.player_count != self.info.player_count:
            return True
        else:
            return False
