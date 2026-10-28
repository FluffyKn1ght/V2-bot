import random

from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot

class GrokIsThisTrueSlashCommand(V2BotCog):
    @commands.slash_command(
        name="grok",
        description="grok",
    )
    async def grok(self, inter: ApplicationCommandInteraction):
        pass

    @grok.sub_command(
        name="isthistrue",
        description="checks if this is factual information"
    )
    async def grok_is_this_true(self, inter: ApplicationCommandInteraction):
        await inter.response.send_message(random.choice(["yes", "yes", "yes", "yes", "yes", "no", "no", "no", "no", "no", "dih"]))

def setup(bot: V2Bot):
    bot.add_cog(GrokIsThisTrueSlashCommand(bot))
