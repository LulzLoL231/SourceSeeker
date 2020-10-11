# -*- coding: utf-8 -*-
# SourceSeeker – utilites
# Author: LulzLoL231
from logging import getLogger, getLevelName, basicConfig, INFO, DEBUG
from a2s.info import ainfo, SourceInfo
from typing import Union

from config import Config


def log(msg: str, level: str = 'INFO', func: Union[str, None] = None) -> None:
    '''log: make log message.

    Args:
        msg (str): Log message.
        level (str): Log level. Defaults to 'INFO'.
        func (Union[str, None]): Function name. Defaults to None.
    '''
    basicConfig(level=DEBUG if Config.DEBUG else INFO,
                format='[%(asctime)s] %(levelname)s | %(name)s | %(message)s')
    log = getLogger('SourceSeeker')
    if func:
        log = getLogger(f'SourceSeeker::{func}')
    log.log(getLevelName(level.upper()), msg)


async def getServerInfo(address: tuple) -> Union[SourceInfo, None]:
    '''getServerInfo: returns SourceInfo about SourceServer or None if connection unsuccessfull.

    Args:
        address (tuple): server ip & port in tuple.

    Returns:
        SourceInfo: Information about SourceServer.
    '''
    info = None
    iter = 0
    while True:
        try:
            info = await ainfo(address)
        except Exception as e:
            log('Error while trying get ServerInfo from '
                f'{address[0]}:{address[1]} with error: {str(e)}',
                'error', 'getServerInfo')
            if iter >= 5:
                return None
            else:
                iter += 1
                continue
        else:
            break
    return info


def getFastConnectURI(address: tuple) -> str:
    '''getFastConnectURI: returns steam fast connect URI in format `steam://connect/IP:PORT`.

    Args:
        address (tuple): server ip & port in tuple.

    Returns:
        str: steam fast connect URI
    '''
    return f'steam://connect/{address[0]}/{address[1]}'
