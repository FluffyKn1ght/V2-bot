from disnake.channel import TextChannel
from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class TalkSlashCommand(V2BotCog):
    @commands.slash_command(name="talk", description="fdkjdsjksdkj")
    async def talk_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        text: str = Param(desc="the text to fdhmjhdfjkdfv"),
    ):
        await inter.channel.send(text)
        await inter.response.send_message(":+1:", ephemeral=True)


def setup(bot: V2Bot):
    bot.add_cog(TalkSlashCommand(bot))
