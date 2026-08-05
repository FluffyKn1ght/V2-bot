import os
import random

from disnake.abc import Messageable
from disnake.file import File
from disnake.message import Message

from cogs.v2cog import V2BotCog
from main import V2Bot


class Bully(V2BotCog):
    async def bully(
        self, dirname: str, channel: Messageable, reply_to: Message | None = None
    ):
        files = []

        for file in os.listdir(f"./medihha/{dirname}"):
            fullpath = os.path.join(f"./medihha/{dirname}", file)
            if os.path.isfile(fullpath):
                files.append(fullpath)

        if reply_to:
            await channel.send(
                ":3", file=File(random.choice(files)), reference=reply_to
            )
        else:
            await channel.send(":3", file=File(random.choice(files)))


def setup(bot: V2Bot):
    bot.add_cog(Bully(bot))
