import io

from disnake import File
from disnake.ext import commands
from disnake.ext.commands.bot import InteractionBot
from disnake.ext.commands.cog import Cog
from disnake.interactions.application_command import ApplicationCommandInteraction
import httpx

from cogs.v2cog import V2BotCog
from main import V2Bot


class FoxSlashCommand(V2BotCog):
    @commands.slash_command(name="fox", description="sends a random fxoe picture :3c")
    async def fox_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()

        async with httpx.AsyncClient() as client:
            response = await client.get("https://randomfox.ca/floof/")

        if response.status_code >= 400:
            raise RuntimeError(f"Image info request failed with {response.status_code}")

        img_info = response.json()

        async with httpx.AsyncClient() as client:
            dl_response = await client.get(img_info["image"])

        if dl_response.status_code >= 400:
            raise RuntimeError(f"Download request failed with {response.status_code}")

        img_data = dl_response.read()

        await inter.edit_original_response(
            f"link to fxoe image: <{img_info["link"]}> \\*yip\\* :3c :fox:",
            file=File(io.BytesIO(img_data), filename="fxoe.jpg"),
        )


def setup(bot: V2Bot):
    bot.add_cog(FoxSlashCommand(bot))
