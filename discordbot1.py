#!/usr/bin//env python3
# -*- coding: utf-8 -*-

import os
import discord

import trans

from mcstatus import MinecraftServer

CMD_PREFIX = "\\"
TRANSLATE_CMD = CMD_PREFIX + "t "

class MyClient(discord.Client):
    """discord bot class"""

    async def on_ready(self):
        """起動時に通知してくれる処理"""
        print("ログインしました")

    async def on_message(self, message):
        """発言された際に発火するイベント"""
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


if __name__ == "__main__":
    # botの接続と起動
    client = MyClient()
    # （tokenにはbotアカウントのアクセストークンを入れてください）
    client.run(os.environ["MC_BOT_KEY"])
