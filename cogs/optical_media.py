from disnake.ext.commands.cog import Cog
from disnake.file import File
from disnake.message import Message

from cogs.v2cog import V2BotCog
from main import V2Bot


class OpticalMediaBAD(V2BotCog):
    @Cog.listener("on_message")
    async def optical_media_bad_msg_listener(self, msg: Message):
        if not self.bot.can_j_in_channel(msg.channel.id):
            return

        if msg.content == "optical media":
            await msg.reply("# BAD", file=File("./medihha/optical-media-bad.gif"))

def setup(bot: V2Bot):
    bot.add_cog(OpticalMediaBAD(bot))