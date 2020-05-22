# discordpy-startup
# -*- coding: utf-8 -*-
import sys
import discord
import aiohttp
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

class Data:
    id_list = []

gch = Data()

@client.event
async def on_ready():

    # 起動後の初期処理の実行を開始する合図としてステータスを変更
    await client.change_presence(activity=discord.Game(name="起動中( ˘ω˘ ) ｽﾔｧ…"))

    # 使い勝手がいいので起動時の時刻を日本時間で取得
    dateTime = datetime.now(JST)

    # 指定チャンネルに起動ログ（embed）を送信
    ready_chid = 675965627873361930
    ready_ch = client.get_channel(ready_chid)
    embed = discord.Embed(title = "起動ログ")
    embed.timestamp = datetime.now(JST)
    await ready_ch.send(embed = embed)

    # グローバルチャンネルのIDのリストを生成
    path = "data/global_channel/id_data.txt"
    with open(path, mode = "r") as file:
        gch.id_list = [int(i.replace("\n", "")) for i in file.readlines()] 
    print(gch.id_list)
    await client.change_presence(activity=discord.Game(name=f"a:help"))

    
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

    if message.author.bot or message.embeds: 
        return


    # グローバルチャットの会話プログラム
    g_webhook_name = "雑談用" # 2チャンネル間のWebhook名

    if message.channel.id in gch.id_list: #IDが登録されているチャンネルにメッセージが送信されたら

        def another_ch(ch):
            ch_list = []

            for ch_id in gch.id_list:

                if message.channel.id != ch_id:
                    ch = client.get_channel(ch_id)
                    ch_list.append(ch)

            return ch_list

        for channel in another_ch(message.channel):

            if channel == None:
                continue

            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name=g_webhook_name)

            if webhook is None: # 雑談用ってwebhookがなかったら無視
                await channel.create_webhook(name = "雑談用")
                await channel.send("Webhook作ったよ")

            if message.attachments:
                await webhook.send(
                    content=message.content,
                    username=message.author.name,
                    avatar_url=message.author.avatar_url_as(format="png")
                )

                for A in message.attachments:
                    img_embed = discord.Embed()
                    img_embed.set_image(url=A.url)
                    await webhook.send(
                        #content=message.content,
                        embed=img_embed,
                        username=message.author.name,
                        avatar_url=message.author.avatar_url_as(format="png")
                   )

            else:
                await webhook.send(
                    content=message.content,
                    username=message.author.name,
                    avatar_url=message.author.avatar_url_as(format="png")
                )

    # チャンネルのグローバル登録コマンドプログラム
    if message.guild:

        if message.content == "a!add":

            if not message.author.guild_permissions.administrator:
                await message.channel.send("おっと！\n君は管理者権限を持ってないから追加は出来ないよ。")
                return

            channel = message.channel
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name=g_webhook_name)

            if webhook is None: # 雑談用ってwebhookがなかったら無視

                try：
                    await channel.create_webhook(name = "雑談用")

                except:
                    await channel.send("なんかうまくいかなかった（）")

                else:
                    path = "data/global_channel/id_data.txt"
                    with open(path, mode = "a") as file:
                        file.write(f"\n{channel.id}")
                    ch.id_list.append(channel.id)

                    for id in ch.id_list:
                        ch = client.get_channel(id)
                        await ch.send(f"{channel.name}をグローバルチャンネルに追加したよ！")
                

client.run(TOKEN)
