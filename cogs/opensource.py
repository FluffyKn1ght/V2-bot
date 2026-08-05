from cogs.v2cog import V2BotCog
from main import V2Bot


class OpenSourceSlashCommand(V2BotCog):
    pass


def setup(bot: V2Bot):
    bot.add_cog(OpenSourceSlashCommand(bot))
