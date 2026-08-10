from disnake.colour import Color
from disnake.embeds import Embed
from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction
import httpx

from cogs.v2cog import V2BotCog
from main import V2Bot

MAX_DEFINITION_COUNT = 5
RETRY_COUNT = 3


class DictionaryLookupSlashCommand(V2BotCog):
    @commands.slash_command(
        name="word", description="lookup a word via freedictonary api"
    )
    async def word_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        word: str = Param(desc="word to look up"),
    ):
        await inter.response.defer(ephemeral=True)

        retries = 0
        while True:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                )

                if response.status_code == 502:
                    if retries < RETRY_COUNT:
                        self.bot.log(
                            f"got 502 from freedictionary api, retrying ({retries+1}/3)"
                        )
                        retries += 1
                        continue
                    else:
                        self.bot.log(
                            "okay i fucking give up here's my two weeks (max retries reached)"
                        )

                        await inter.response.edit_message(
                            "api error, please try again :<"
                        )
                        return
                else:
                    break

        if response.status_code >= 400:
            raise RuntimeError(f"Request failed with {response.status_code}")

        data = response.json()

        pronounce = ""
        for pronounce_variant in data:
            if "audio" in pronounce_variant.keys():
                pronounce = pronounce_variant["audio"]
                break

        embed = Embed(
            title=f"{word}",
            description=f"Phonetic: {data[0]["phonetic"]}\n{f"Pronounciation: [click here to listen](<{pronounce}>)" if pronounce else "No pronounciation available..."}",
            color=Color(0x9F00FF),
        )

        for meaning_data in data[0]["meanings"]:
            value = ""

            def_count = 0
            for definition in meaning_data["definitions"]:
                if def_count >= MAX_DEFINITION_COUNT:
                    break

                synonyms = ""
                for synonym in definition["synonyms"]:
                    if not synonyms:
                        synonyms += f"**{synonym}**" + " "
                    else:
                        synonyms += synonym + " "

                antonyms = ""
                for antonym in definition["antonyms"]:
                    if not antonyms:
                        antonyms += f"**{antonym}**" + " "
                    else:
                        antonyms += antonym + " "

                value += f"{f"**{definition["definition"]}**" if not def_count else definition["definition"]}\n{f"Similar to: {synonyms}\n" if synonyms else ""}{f"Opposite to: {antonyms}\n" if antonyms else ""}{f"Example: {definition["example"]}\n" if "example" in definition.keys() else ""}\n"

                def_count += 1

            embed.add_field(
                name=f"Meanings as {meaning_data["partOfSpeech"]}",
                value=value,
                inline=False,
            )

        await inter.edit_original_response(embed=embed)


def setup(bot: V2Bot):
    bot.add_cog(DictionaryLookupSlashCommand(bot))
