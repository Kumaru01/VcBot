#    This file is part of the Vc distribution.
#    Copyright (c) 2021 kaif-00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/kaif-00z/VcBot/blob/main/License> .


import time
from logging import DEBUG, INFO, basicConfig, getLogger, warning

import asyncio
import youtube_dl
from pytgcalls import GroupCallFactory
from pytgcalls.exceptions import GroupCallNotFoundError
from telethon import Button, TelegramClient, errors, events
from telethon.sessions import StringSession

from .config import *

basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO)
LOGS = getLogger(__name__)


try:
    user = TelegramClient(StringSession(Var.SESSION), Var.API_ID, Var.API_HASH)
except Exception as e:
    LOGS.info("Environment vars are missing")
    LOGS.info(str(e))
    exit()
