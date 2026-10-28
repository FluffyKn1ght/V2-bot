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
    def grok(self, inter: ApplicationCommandInteraction):
        pass

    @grok.sub_command(
        name="is",
        description="is"
    )
    def grok_is(self, inter: ApplicationCommandInteraction):
        pass

    @grok_is.sub_command(
        name="this",
        description="this"
    )
    def grok_is_this(self, inter: ApplicationCommandInteraction):
        pass

    @grok_is_this.sub_command(
        name="true",
        description="true"
    )
    def grok_is_this_true(self, inter: ApplicationCommandInteraction):
        inter.response.send_message(random.choice(["yes", "yes", "yes", "yes", "yes", "no", "no", "no", "no", "no", "dih"]))

def setup(bot: V2Bot):
    bot.add_cog(GrokIsThisTrueSlashCommand(bot))
