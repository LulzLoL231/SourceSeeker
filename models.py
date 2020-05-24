# -*- coding: utf-8 -*-
# SourceSeeker – models
# Author: LulzLoL231
import os
from datetime import datetime

import a2s
from discord import Embed, Colour

from utils import log


async def GetServerInfo(addr):
    '''Coroutine. Request source server info through a2s protocol.

    Args:
        addr: Source server str(IP) and int(PORT) in tuple.

    Returns:
        if successfull:
            a2s.SourceInfo
        else:
            None
    '''
    recv = False
    iter = 0
    while recv != True:
        try:
            i = a2s.info(addr)
        except Exception as e:
            log('GetServerInfo', f'Server: {str(addr)} – {e}', 'warn')
            if iter <= 5:
                return None
            else:
                iter += 1
                continue
        else:
            recv = True
            return i


def GetFastConnectURI(addr):
    '''Get steam connect uri in format `steam://connect//IP:PORT`.

    Args:
        addr: Source server str(IP) and int(PORT) in tuple.

    Returns:
        Steam connect uri.
    '''
    return f'steam://connect/{addr[0]}:{addr[1]}'


def GetEmbedDict(server=None, SteamURI=None, inline=False, offline=False):
    '''Get embed `ready` dict, for transfor to discord.Embed.

    Args:
        server  : Server object instance.
        SteamURI: steam connect uri in str.
        inline  : select embed style. boolean.
        offline : select embed style, if server online or not. boolean.

    Returns:
        dict.
    '''
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
    '''Source Server instance. For storage server address, memo, chhannels and etc.

    Args:
        address : Source server str(IP) and int(PORT) in tuple.
        channels: Discord channels ids in tuple.
        refresh : Set seeking style: refresh `one` msg, or send new msg everytime, when source server map is change. boolean.
        inline  : Set embed style. boolean.
        memo    : Set source server name in str. optional.
    '''
    def __init__(self, address, channels, refresh, inline, memo=None):
        '''Init class object.'''
        self.address = address
        self.info = None
        if self.info is None:
            if memo is None:
                self.server_name = 'Unknown Source Server'
            else:
                self.server_name = memo
        self.SteamURI = GetFastConnectURI(address)
        self.channels = channels
        self.inline = inline
        self.refresh = refresh
        self.memo = memo

    def FromTuple(tuple):
        '''Get class instance from tuple.

        Args:
            tuple: server info in tuple(tuple(IP, PORT), tuple(CHANNELS), bool(INLINE), bool(REFRESH), str(MEMO))

        Returns:
            models.Server instance.
        '''
        if len(tuple) == 5:
            return Server(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4])

    def GetEmbed(self):
        '''Get discord.Embed for this Server.

        Returns:
            discord.Embed.
        '''
        if self.info is None:
            return Embed.from_dict(GetEmbedDict(offline=self.server_name, SteamURI=self.SteamURI))
        return Embed.from_dict(GetEmbedDict(self.info, self.SteamURI, self.inline))

    async def IsMapChange(self):
        '''Coroutine. Get boolean for event server map change.

        Returns:
            if GetServerInfo.map_name != self.info.map_name:
                return True
            else:
                return False
        '''
        seek = await GetServerInfo(self.address)
        if (seek is None) or (self.info is None):
            return True
        elif seek.map_name != self.info.map_name:
            return True
        else:
            return False

    async def UpdateInfo(self):
        '''Coroutine. Update self.info.

        Returns:
            True. Everytime.'''
        self.info = await GetServerInfo(self.address)
        return True

    async def IsPlayerCountChange(self):
        '''Coroutine. Get boolean for event server player_count change.

        Returns:
            if GetServerInfo.player_count != self.info.player_count:
                return True
            else:
                return False
        '''
        seek = await GetServerInfo(self.address)
        if (seek is None) or (self.info is None):
            return True
        elif seek.player_count != self.info.player_count:
            return True
        else:
            return False
