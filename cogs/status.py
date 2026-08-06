import random

from disnake.activity import Activity
from disnake.ext import tasks
from disnake.types.activity import ActivityType

from cogs.v2cog import V2BotCog
from main import V2Bot


class StatusManager(V2BotCog):
    def __init__(self, bot: V2Bot) -> None:
        super().__init__(bot)

        self.statuses = self.bot.config["statuses"]
        self.current_status = ""
        self.change_interval = self.bot.config["status_change_interval"]

        self.status_change_task.change_interval(seconds=self.change_interval)

        self.status_change_task.start()

    @tasks.loop(seconds=14400.0)
    async def status_change_task(self):
        while True:
            new_status = random.choice(self.statuses)
            if new_status == self.current_status:
                continue
            break

        self.current_status = new_status

        await self.bot.change_presence(activity=Activity(name=self.current_status))

    @status_change_task.before_loop
    async def before_status_loop_task(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

    def reload_status_config(self):
        self.statuses = self.bot.config["statuses"]
        self.current_status = ""
        self.last_status = ""
        self.change_interval = self.bot.config["status_change_interval"]

        self.status_change_task.change_interval(seconds=self.change_interval)


def setup(bot: V2Bot):
    bot.add_cog(StatusManager(bot))
