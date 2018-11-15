#!/usr/bin//env python3
# -*- coding: utf-8 -*-

import os
import re

# pip
import discord

# my module
import trans
import joke

# pip
from mcstatus import MinecraftServer

CMD_PREFIX = "\\"
TRANSLATE_CMD = CMD_PREFIX + "t "
JOKE_CMD = CMD_PREFIX + "g "

def _extract_minecraft_chat(chat):
    """マイクラチャットから入力値\t のみを抽出する
    player » \t english translation test (￥t 園gl位sh tr案sl阿智音 手st)
    ->english translation test"""

    if re.search(r"\(.*\)", chat):
        # LunaChat is on
        match = re.search("»\s\\\\t\s(.*)\s\(", chat)
        if match:
            return match.group(1)
    else:
        # LunaChat is off
        match = re.search("»\s\\\\t\s(.*)", chat)
        if match:
            return match.group(1)

    return None

class MyClient(discord.Client):
    """discord bot class"""

    async def on_ready(self):
        """起動時に通知してくれる処理"""
        print("ログインしました")

    async def on_message(self, message):
        """発言された際に発火するイベント"""

        if message.author == client.user:
            # Bot自身の発言を無視
            return

        # マイクラサーバ内からのチャットを抽出
        minecraft_chat = _extract_minecraft_chat(message.content)

        if message.content.startswith(CMD_PREFIX + "neko"):
            reply = 'にゃーん '
            server = MinecraftServer.lookup("mc.toraden.com:25565")
            status = server.status()
            reply += "mc.toraden.comのプレーヤーは {0} players 居るよ！"\
                     "速さは、replied in {1} ms だよ！"\
                     .format(status.players.online, status.latency)
            await client.send_message(message.channel, reply)
        elif message.content.startswith(TRANSLATE_CMD):
            # 翻訳してみる
            t = trans.Trans(message.content.replace(TRANSLATE_CMD, ""))
            await client.send_message(message.channel, t.translate())
        elif minecraft_chat:
            # マイクラサーバ内からのチャット翻訳
            t = trans.Trans(minecraft_chat)
            await client.send_message(message.channel, t.translate())
        elif message.content.startswith(JOKE_CMD) \
             or re.search("»\s\\\\g\s", message.content):
            # ジョークレスポンス
            j = joke.Joke()
            await client.send_message(message.channel, j.choice())

if __name__ == "__main__":
    # botの接続と起動
    client = MyClient()
    # （tokenにはbotアカウントのアクセストークンを入れてください）
    client.run(os.environ["MC_BOT_KEY"])
