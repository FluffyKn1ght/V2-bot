from disnake.ext.commands.cog import Cog

from main import V2Bot


class V2BotCog(Cog):
    def __init__(self, bot: V2Bot) -> None:
        self.bot: V2Bot = bot
