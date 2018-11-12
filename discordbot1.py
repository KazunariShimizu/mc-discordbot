#!/usr/bin//env python3
# -*- coding: utf-8 -*-

import os
import discord # インストールした discord.py

from mcstatus import MinecraftServer

client = discord.Client() # 接続に使用するオブジェクト

# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')

# 「/neko」と発言したら「にゃーん」が返る処理
@client.event
async def on_message(message):
    if message.content.startswith('/neko'):
        reply = 'にゃーん '
        server = MinecraftServer.lookup("mc.toraden.com:25565")
        status = server.status()
        reply += "mc.toraden.comのプレーヤーは {0} players 居るよ！速さは、replied in {1} ms だよ！".format(status.players.online, status.latency)
        await client.send_message(message.channel, reply)

# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.run(os.environ["MC_BOT_KEY"])
