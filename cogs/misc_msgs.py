import random

from disnake.ext import commands
from disnake.file import File
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class MiscMessages(V2BotCog):
    @commands.slash_command(name="grandpa", description="actual fossil")
    async def grandpa_slash_command(self, inter: ApplicationCommandInteraction):
        if random.randint(1, 10) > 8:
            await inter.response.send_message(
                "granola bar :revolving_hearts::revolving_hearts:",
                file=File("./medihha/grandpa/granolabar.jpg"),
            )
        else:
            await inter.response.send_message(
                "grandoa :revolving_hearts::revolving_hearts:",
                file=File("./medihha/grandpa/grandpaluci.png"),
            )

    @commands.slash_command(name="spoon", description="the spoon")
    async def spoon_slash_command(self, inter: ApplicationCommandInteraction):
        r = random.randint(1, 10)

        if r == 10:
            await inter.response.send_message(
                file=File("./medihha/spoon/whatthefuckspoon.gif")
            )
        elif r >= 8:
            await inter.response.send_message(
                file=File("./medihha/spoon/actualspoon.png")
            )
        else:
            await inter.response.send_message(file=File("./medihha/spoon/spoon.png"))

    @commands.slash_command(
        name="opensource", description="me when free and open source software: 👍"
    )
    async def open_source_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.send_message("https://github.com/fluffykn1ght/v2-bot :3")


def setup(bot: V2Bot):
    bot.add_cog(MiscMessages(bot))
