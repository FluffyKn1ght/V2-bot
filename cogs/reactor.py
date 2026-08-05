from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction
from disnake.message import Message
from disnake.user import User

from cogs.v2cog import V2BotCog
from main import V2Bot


class Reactor(V2BotCog):
    def __init__(self, bot: V2Bot) -> None:
        super().__init__(bot)

        self.selected_messages: dict[int, int] = {}

    @commands.message_command(name="select meassg")
    async def select_message_message_command(
        self, inter: ApplicationCommandInteraction, message: Message
    ):
        self.selected_messages[inter.user.id] = message.id

        await inter.response.send_message(":+1:", ephemeral=True)

    @commands.slash_command(
        name="react_to_msg", description="makes the bot react to a selected message"
    )
    async def react_to_msg_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        emojis: str = Param(desc='emojis (one or multiple split by ","s)'),
    ):
        if not inter.user.id in self.selected_messages.keys():
            await inter.response.send_message(
                "you havent selected a message vro :wilted_rose:", ephemeral=True
            )
            return

        await inter.response.defer(ephemeral=True)

        try:
            msg = await inter.channel.fetch_message(
                self.selected_messages[inter.user.id]
            )
        except Exception:
            await inter.response.send_message(
                "the message is in the wrong channel you orange cat :wilted_rose:",
                ephemeral=True,
            )
            return

        for emoji in emojis.split(","):
            try:
                await msg.add_reaction(emoji)
            except Exception:
                await inter.response.send_message(
                    f"okay vro wtf is `{emoji}` :wilted_rose:", ephemeral=True
                )
                return

        await inter.edit_original_response("okiiii i weacted to da meassg :3")


def setup(bot: V2Bot):
    bot.add_cog(Reactor(bot))
