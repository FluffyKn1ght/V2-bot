from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class ReloadConfigCommand(V2BotCog):
    @commands.slash_command(name="reloadcfg", description="reloads the config")
    async def reloadcfg_command(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)

        print("reloading config...")
        self.bot.reload_config()
        print("reloaded config ok!")

        await inter.edit_original_response(":+1:")


def setup(bot: V2Bot):
    bot.add_cog(ReloadConfigCommand(bot))
