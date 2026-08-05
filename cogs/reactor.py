import random
import re

from disnake.ext import commands
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction
from disnake.message import Message
from disnake.user import User

from cogs.v2cog import V2BotCog
from main import V2Bot


class Reactor(V2BotCog):
    @commands.slash_command(
        name="react_to_msg", description="makes the bot react to a selected message"
    )
    async def react_to_msg_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        emojis_or_rule: str = Param(
            desc='emojis (one or multiple split by ","s) or react rule name'
        ),
    ):
        if not inter.user.id in self.bot.selected_messages.keys():
            await inter.response.send_message(
                "you havent selected a message vro :wilted_rose:", ephemeral=True
            )
            return

        await inter.response.defer(ephemeral=True)

        try:
            msg = await inter.channel.fetch_message(
                self.bot.selected_messages[inter.user.id]
            )
        except Exception:
            await inter.response.send_message(
                "the message is in the wrong channel you orange cat :wilted_rose:",
                ephemeral=True,
            )
            return

        if emojis_or_rule in self.bot.config["rules"].keys():
            reacts = self.bot.config["rules"][emojis_or_rule]["reactions"]
            random.shuffle(reacts)

            for react in reacts:
                await msg.add_reaction(react)
        else:
            for emoji in emojis_or_rule.split(","):
                try:
                    await msg.add_reaction(emoji)
                except Exception:
                    await inter.response.send_message(
                        f"okay vro wtf is `{emoji}` :wilted_rose:", ephemeral=True
                    )
                    return

        await inter.edit_original_response("okiiii i weacted to da meassg :3")

    @Cog.listener("on_message")
    async def run_message_react_rules(self, msg: Message):
        if msg.channel.id in self.bot.config["channel_blacklist"]:
            return

        for rule_name in self.bot.config["rules"]:
            rule = self.bot.config["rules"][rule_name]

            match_found = False
            for expr in rule["keywords"]:
                result = re.search(expr, msg.content)
                if result:
                    match_found = True
                    break

            if match_found:
                for bully_rule in self.bot.config["bully"]:
                    if (
                        bully_rule["uid"] == msg.author.id
                        and bully_rule["rule"] == rule_name
                    ):
                        await self.bot.get_cog("Bully").bully(bully_rule["dirname"], msg.channel, msg)  # type: ignore

                reacts = rule["reactions"]
                random.shuffle(reacts)

                for react in reacts:
                    await msg.add_reaction(react)


def setup(bot: V2Bot):
    bot.add_cog(Reactor(bot))
