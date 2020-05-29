class DiscordThread:

    def __init__(self, client, message):
        # Thread化するチャネル名リスト
        self.channel_names = ['要望', '不具合報告', '質問']

        # カテゴリ名からチャネルを取得する方法は無い？
        # self.category_name = 'スレッド'
        self.category_id = 715916859303526461  # 'スレッド' カテゴリのID

        self.client = client
        self.message = message

    async def create(self):
        if self.message.channel.name not in self.channel_names:
            return

        category_channel = self.client.get_channel(self.category_id)

        # In name: Must be between 1 and 100 in length.
        channel_name = f'{self.message.channel.name}：{self.message.content}'[:100]

        payload = {'name': channel_name, 'category': category_channel, 'position': 0}
        text_channel = await self.message.guild.create_text_channel(**payload)
        await text_channel.send(self.message.jump_url)
        await self.client.get_channel(self.category_id).edit(position=0)
        await self.message.channel.send(text_channel.mention)
