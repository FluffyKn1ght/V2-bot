import json
import random
from typing import Any

from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.file import File
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class KDEDragonSlashCommand(V2BotCog):
    def __init__(self, bot: V2Bot) -> None:
        super().__init__(bot)

        self.catalogue: list[dict[str, Any]] = []

    @commands.slash_command(
        name="kde_dragon", description="sends a random kde dragon picture :3"
    )
    async def kdedragon_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        dragon_type: str = Param(
            desc="which dragon to send (random if not specified)",
            choices=["konqi", "katie", "kori", "other"],
            default="idfk",
        ),
    ):
        await inter.response.defer()

        valid_pics = []
        for entry in self.catalogue:
            if dragon_type != "idfk":
                if not dragon_type in entry["tags"]:
                    continue

            valid_pics.append(entry)

        pic = random.choice(valid_pics)

        await inter.edit_original_response(
            f"here is your {dragon_type if dragon_type != "idfk" and dragon_type != "other" else "kde dragon"} picture! :3\n-# please visit [this page](<https://community.kde.org/Promo/Material/Mascots>) for licensing/credit/other info\n-# a full quality version of this image is available [here](<{pic["url"]}>)",
            file=File(f"./medihha/kde-dragons/{pic["file"]}"),
        )

    def reload_catalogue(self):
        self.catalogue = json.loads(
            self.bot.read_file("./medihha/kde-dragons/catalogue.json")
        )


def setup(bot: V2Bot):
    bot.add_cog(KDEDragonSlashCommand(bot))
