#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random

JOKE_RESPONSE_FILE = os.path.join(os.path.dirname(__file__), "jokes.txt")

class Joke:
    """ジョークレスポンスを返すクラス"""


    def __init__(self):
        try:
            with open(JOKE_RESPONSE_FILE, "r") as f:
                self.jokes = f.readlines()
        except FileNotFoundError:
            print("{}が存在しません".format(JOKE_RESPONSE_FILE))

    def choice(self):
        """ジョークを1つ選んで返す"""
        return random.choice(self.jokes)

if __name__ == "__main__":
    j = Joke()
    print(j.choice())
