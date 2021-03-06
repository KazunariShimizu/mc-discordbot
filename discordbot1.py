#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging

# pip
import discord

# my module
from lib import trans, joke, discord_thread

# pip
from mcstatus import MinecraftServer

LOG_FILE = os.path.join(os.path.dirname(__file__), "discord.log")
DOMAIN = "toraden.com"
PORT = 25565

logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename=LOG_FILE, encoding="utf-8", mode="a")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

CMD_PREFIX = "\\"
TRANSLATE_CMD = CMD_PREFIX + "t "
JOKE_CMD = CMD_PREFIX + "g"
NEKO_CMD = CMD_PREFIX + "neko"


def _extract_minecraft_chat(chat):
    """マイクラチャットから入力値\t のみを抽出する
    player » \t english translation test (￥t 園gl位sh tr案sl阿智音 手st)
    ->english translation test"""

    if re.search(r"\(.*\)", chat):
        # LunaChat is on
        match = re.search(r"»\s\\t\s(.*)\s\(", chat)
        if match:
            return match.group(1)
    else:
        # LunaChat is off
        match = re.search(r"»\s\\t\s(.*)", chat)
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

        my_thread = discord_thread.DiscordThread(self, message)
        await my_thread.create()

        # マイクラサーバ内からのチャットを抽出
        minecraft_chat = _extract_minecraft_chat(message.content)

        if message.content.startswith(NEKO_CMD) \
             or re.search(r"»\s\\neko", message.content):
            server = MinecraftServer.lookup(DOMAIN + ":" + str(PORT))
            status = server.status()
            reply = "にゃーん " + DOMAIN + "のプレーヤーは {0} players 居るよ！"\
                "速さは、replied in {1} ms だよ！"\
                .format(status.players.online, status.latency)
            await message.channel.send(reply)
        elif message.content.startswith(TRANSLATE_CMD):
            # 翻訳してみる
            t = trans.Trans(message.content.replace(TRANSLATE_CMD, ""))
            await message.channel.send(t.translate())
        elif minecraft_chat:
            # マイクラサーバ内からのチャット翻訳
            t = trans.Trans(minecraft_chat)
            await message.channel.send(t.translate())
        elif message.content.startswith(JOKE_CMD) \
             or re.search(r"»\s\\g", message.content):
            # ジョークレスポンス
            j = joke.Joke()
            await client.send(message.channel, j.choice())


if __name__ == "__main__":
    # botの接続と起動
    client = MyClient()
    # （tokenにはbotアカウントのアクセストークンを入れてください）
    client.run(os.environ["MC_BOT_KEY"])
