from disnake.ext.commands.cog import Cog
from disnake.member import Member
from disnake.message import Message
from disnake.role import Role

from cogs.v2cog import V2BotCog
from main import V2Bot


class FleshPrison(V2BotCog):
    @Cog.listener("on_message")
    async def do_fleshprison_thingy(self, msg: Message):
        for role_id in self.bot.config["horny"].keys():
            role_id = int(role_id)
            for role in msg.author.roles:  # type: ignore
                if role.id == role_id:
                    if not msg.channel.id in self.bot.config["horny"][str(role_id)]:
                        await msg.delete()

                continue

    @Cog.listener("on_member_update")
    async def curse_of_binding(self, before: Member, after: Member):
        for role_id in self.bot.config["horny"].keys():
            try:
                role = await after.guild.fetch_role(role_id)
            except Exception:
                continue

            if role in before.roles and not role in after.roles:
                await after.add_roles(role)


def setup(bot: V2Bot):
    bot.add_cog(FleshPrison(bot))
