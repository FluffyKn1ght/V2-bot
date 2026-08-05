import io

from disnake import File
from disnake.ext import commands
from disnake.ext.commands.bot import InteractionBot
from disnake.ext.commands.cog import Cog
from disnake.interactions.application_command import ApplicationCommandInteraction
import httpx

from cogs.v2cog import V2BotCog
from main import V2Bot


class CatSlashCommand(V2BotCog):
    @commands.slash_command(name="cat", description="sends a random ktiiy picture :3c")
    async def cat_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()

        async with httpx.AsyncClient() as client:
            response = await client.get("https://cataas.com/cat?json=1")

        if response.status_code >= 400:
            raise RuntimeError(f"Request failed with {response.status_code}")

        img_info = response.json()

        await inter.edit_original_response(
            f"here's your [ktiiy image]({img_info["url"]}) :3 :cat:",
        )


def setup(bot: V2Bot):
    bot.add_cog(CatSlashCommand(bot))
