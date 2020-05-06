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
    embed = discord.Embed(title = "起動ログ")
    embed.timestamp = datetime.now(JST)
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

    if message.author.bot: 
        return 
    if message.embeds:
        return
    g_webhook_name = "雑談用" # 2チャンネル間のWebhook名
    CHANNEL_ID = [675965627873361930,
                  607213936982622229,
                  674983698080202797]
    if message.channel.id in CHANNEL_ID: #IDが登録されているチャンネルにメッセージが送信されたら
        def another_ch(ch):
            CHANNEL_ID = [
                675965627873361930,
                607213936982622229,
                674983698080202797]
            ch_1 = client.get_channel(CHANNEL_ID[0])
            ch_2 = client.get_channel(CHANNEL_ID[1])
            ch_3 = client.get_channel(CHANNEL_ID[2])
            ch_list = []
            if ch.id == ch_1.id:
                ch_list.append(ch_2)
                ch_list.append(ch_3)
            elif ch.id == ch_2.id:
                ch_list.append(ch_1)
                ch_list.append(ch_3)
            elif ch.id == ch_3.id:
                ch_list.append(ch_2)
                ch_list.append(ch_3)
            return ch_list
        for channel in another_ch(message.channel):
            if channel == None:
                continue
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name=g_webhook_name) 
            if webhook is None: # 雑談用ってwebhookがなかったら無視
                await channel.create_webhook(name = "雑談用")
                await channel.send("Webhook作ったよ")
            await webhook.send(
                content=message.content,
                username=message.author.name,
                avatar_url=message.author.avatar_url_as(format="png")
            )   

client.run(TOKEN)
