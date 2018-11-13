#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from py_translator import Translator


class Trans:

    def __init__(self, txt):
        self.txt = txt
        self.translated = None
        self.translator = Translator()

    def en_to_ja(self):
        self.translated = self.translator.translate(
            text=self.txt, dest="ja").text

    def ja_to_en(self):
        self.translated = self.translator.translate(
            text=self.txt, dest="en").text

    def translate(self):

        # 0x00 - 0x7F is ascii character code point
        if re.search(r"^[\x00-\x7F]+$", self.txt):
            self.en_to_ja()
        else:
            self.ja_to_en()

        return self.translated


if __name__ == "__main__":
    txt = "Hello world"
    t = Trans(txt)
    print(t.translate())

    txt = "こんにちは世界"
    t = Trans(txt)
    print(t.translate())
