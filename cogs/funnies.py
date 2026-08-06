from disnake.ext.commands.cog import Cog
from disnake.file import File
from disnake.message import Message

from cogs.v2cog import V2BotCog
from main import V2Bot


class Funnies(V2BotCog):
    @Cog.listener("on_message")
    async def do_funny_message(self, msg: Message):
        if not self.bot.can_j_in_channel(msg.channel.id):
            return

        for text in self.bot.config["funnies"]:
            if msg.content == text:
                funny_response = self.bot.config["funnies"][text]

                if type(funny_response) is str:
                    await msg.channel.send(funny_response)
                else:
                    files = []
                    for fname in funny_response["files"]:
                        files.append(File(f"./medihha/{fname}"))

                    await msg.channel.send(funny_response["content"], files=files)

                return


def setup(bot: V2Bot):
    bot.add_cog(Funnies(bot))
