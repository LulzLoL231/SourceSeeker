# -*- coding: utf-8 -*-
# SourceSeeker – utilites
# Author: LulzLoL231
import builtins
import logging
from datetime import datetime

import config

def log(func, message, type=None):
    template_stdin = '[ {} ] | {} | func: {} | {}'
    if config.debug is True:
        if type is None:
            type = 'info'
        builtins.print(template_stdin.format(str(datetime.now()), type, func, message))
    else:
        logger = logging.getLogger("SourceSeeker")
        logger.setLevel(config.logging_level)
        fh = logging.FileHandler("sourceseeker.log")
        form = logging.Formatter('[ %(asctime)s ] | %(levelname)s | func: %(message)s')
        fh.setFormatter(form)
        logger.addHandler(fh)
        if type is None:
            type = 'info'
        eval(f'logger.{type}("\'{func}\' | {message}")')