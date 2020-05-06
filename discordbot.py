# discordpy-startup
# -*- coding: utf-8 -*-
import sys
import discord
import random
import asyncio
import time
import datetime
import urllib.request
import json
import re
import os
import traceback
import math

from discord.ext import tasks
from datetime import datetime, timedelta, timezone

import logging


JST = timezone(timedelta(hours=+9), 'JST') # タイムゾーンの生成
client = discord.Client() 
TOKEN = os.environ['DISCORD_BOT_TOKEN'] # botのtoken(heroku参照)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="起動中( ˘ω˘ ) ｽﾔｧ…"))
    ready_chid = 675965627873361930
    ready_ch = client.get_channel(ready_chid)
    dateTime = datetime.now(JST)
    embed = discord.Embed(
        title = "起動ログ",
        description = f"{dateTime}")
    await ready_ch.send(embed = embed) #起動ログを指定のチャンネルに送信
    await client.change_presence(activity=discord.Game(name=f"起動完了！"))
    loop.start()
    
@client.event
async def on_member_join(member):
    pass
@client.event
async def on_member_remove(member): 
    pass
@tasks.loop(seconds=10)
async def loop():
    pass
@client.event
async def on_message(message):
    try:
        pass    
    except Exception as error:
        ERROR_TYPE = str(type(error))
        ERROR = str(error)
        embed = discord.Embed(
            title = ERROR_TYPE,
            description = ERROR,
            color = discord.Color.red())
        embed.add_field(
            name = "エラーが出たメッセージ",
            value = message.content)
        embed.timestamp = datetime.now(JST)
        await message.channel.send(embed = embed)
    else:
        pass
client.run(TOKEN)
