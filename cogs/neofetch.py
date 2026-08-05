import subprocess

from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class NeofetchSlashCommand(V2BotCog):
    @commands.slash_command(
        name="neofetch", description="runs neofetch on the bot's server :3"
    )
    async def neofetch_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()

        result = subprocess.run(
            [
                "bash",
                "./utils/invoke-neofetch.sh",
            ],
            capture_output=True,
        )

        await inter.edit_original_response(
            f"```{result.stdout.decode().replace("`", "'")}```"
        )


def setup(bot: V2Bot):
    bot.add_cog(NeofetchSlashCommand(bot))
