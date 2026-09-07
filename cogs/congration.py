import random

from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from cogs.v2cog import V2BotCog
from main import V2Bot


class CongrationSlashCommand(V2BotCog):
    @commands.slash_command(name="congration", description="congration 🍾🍾🍾")
    async def congration_slash_command(self, inter: ApplicationCommandInteraction):
        with open("./medihha/congration.txt", "r") as fp:
            words = fp.readlines()

        word = ""
        while True:
            word = random.choice(words)
            if not word:
                continue
            break

        await inter.response.send_message(
            f"{word.rstrip("\n")} :champagne::champagne::champagne:"
        )


def setup(bot: V2Bot):
    bot.add_cog(CongrationSlashCommand(bot))
