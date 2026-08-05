from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class OpenSourceSlashCommand(V2BotCog):
    @commands.slash_command(
        name="opensource", description="me when free and open source software: 👍"
    )
    async def open_source_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.send_message("https://github.com/fluffykn1ght/v2-bot :3")


def setup(bot: V2Bot):
    bot.add_cog(OpenSourceSlashCommand(bot))
