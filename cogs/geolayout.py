from enum import Enum
import re

from disnake.ext.commands.cog import Cog
from disnake.message import Message

from cogs.v2cog import V2BotCog
from main import V2Bot


class GeoLayOut(V2BotCog):
    def __init__(self, bot: V2Bot) -> None:
        super().__init__(bot)

        self.geolayout: set[int] = set()

    @Cog.listener("on_message")
    async def geolayout_msg_listener(self, msg: Message):
        if msg.author.id == self.bot.user.id:
            return

        if not self.bot.can_j_in_channel(msg.channel.id):
            return

        if msg.channel.id in self.geolayout:
            if msg.content == "out":
                await msg.add_reaction("👍")
            else:
                match_found = False
                for pattern in self.bot.config["geolayout"]:
                    if re.match(pattern, msg.content):
                        await msg.reply(self.bot.config["geolayout"][pattern])
                        match_found = True
                        break

                if not match_found:
                    await msg.reply("fuck you")

            self.geolayout.remove(msg.channel.id)
        elif msg.content.lower() == "geo":
            await msg.reply("lay")
            self.geolayout.add(msg.channel.id)


def setup(bot: V2Bot):
    bot.add_cog(GeoLayOut(bot))
