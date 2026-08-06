from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class SeriousChannels(V2BotCog):
    @commands.slash_command(
        name="srs_channel",
        description="make current channel serious (disables some bot stuff)",
    )
    async def srs_channel_command(self, inter: ApplicationCommandInteraction):
        self.bot.srs_channels.add(inter.channel_id)
        await inter.response.send_message("channel has been /srs'd", ephemeral=True)

    @commands.slash_command(
        name="unsrs_channel", description="make current channel unserious"
    )
    async def unsrs_channel_command(self, inter: ApplicationCommandInteraction):
        try:
            self.bot.srs_channels.remove(inter.channel_id)
        except KeyError:
            pass
        await inter.response.send_message("channel has been un/srs'd", ephemeral=True)


def setup(bot: V2Bot):
    bot.add_cog(SeriousChannels(bot))
