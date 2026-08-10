import io
import os
import traceback
from typing import Any, Callable

from disnake import Intents
from disnake.ext import commands
from disnake.ext.commands import InteractionBot
import json

from disnake.interactions.application_command import ApplicationCommandInteraction
from disnake.message import Message

import sys


class V2Bot(InteractionBot):
    def __init__(self, *args, config_file: str, secrets_file: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.logs = ""

        self.config_file = config_file
        self.config = json.loads(self.read_file(config_file))

        for cog in self.config["cogs"]:
            self.log(f"Loading cog {cog}")
            self.load_extension(f"cogs.{cog}")

        self.secrets: dict[str, Any] = json.loads(self.read_file(secrets_file))

        self.reload_config()

        self.selected_messages: dict[int, int] = {}
        self.srs_channels: set[int] = set()

        @self.event
        async def on_ready():
            self.log(f"Logged in as {self.user.display_name} ({self.user.id})")

        @self.event
        async def on_slash_command_error(
            inter: ApplicationCommandInteraction, e: Exception
        ):
            self.log(
                f"SLASH COMMAND ERROR in {inter.application_command.name}! {e.__class__.__name__}: {e}"
            )

        @self.message_command(name="select meassg")
        async def select_message_message_command(
            inter: ApplicationCommandInteraction, message: Message
        ):
            self.selected_messages[inter.user.id] = message.id

            await inter.response.send_message(":+1:", ephemeral=True)

    def run_bot(self):
        self.run(self.secrets["token"])

    def reload_config(self):
        self.config = json.loads(self.read_file(self.config_file))

        self.get_cog("StatusManager").reload_status_config()  # type: ignore
        self.get_cog("Bully").reload_bully_types()  # type: ignore
        self.get_cog("KDEDragonSlashCommand").reload_catalogue()  # type: ignore

    def can_j_in_channel(self, channel_id: int) -> bool:
        return not (
            channel_id in self.config["channel_blacklist"]
            or channel_id in self.srs_channels
        )

    def log(self, txt: str):
        print(txt)
        self.logs += f"{txt}\n"

        if len(self.logs) > 10000:
            self.logs = self.logs[len(self.logs) - 10000 :]

    @staticmethod
    def read_file(fname: str) -> str:
        with open(fname, "r") as fp:
            return fp.read()


if __name__ == "__main__":
    bot = V2Bot(
        config_file="config.json",
        secrets_file="secrets.json",
        intents=Intents.all(),
    )

    bot.log('"uwu this collar fits so nicely on me" - V2 apparently idfk')
    bot.run_bot()
