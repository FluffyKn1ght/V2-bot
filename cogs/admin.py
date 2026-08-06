from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot


class AdminSlashCommands(V2BotCog):
    @commands.slash_command(
        name="restart_bot", description="[admin only] give em the ol' reliable exit()"
    )
    async def restart_bot_slash_command(self, inter: ApplicationCommandInteraction):
        if not inter.user.id in self.bot.config["admins"]:
            await inter.response.send_message(
                "https://cdn.discordapp.com/attachments/742123470145585253/1533220053254803616/togif.gif?ex=6a75a0b2&is=6a744f32&hm=df2d3fa06adca8ae5d18220efc0449ca6536d41be6e68aeca1289cf18b2057ef&",
                ephemeral=True,
            )
            return

        print(
            f"/restart_bot triggered by {inter.user.display_name} (UID {inter.user.id})"
        )
        await inter.response.send_message(
            "okay :+1: \\*kills himself\\*", ephemeral=True
        )

        exit(1)


def setup(bot: V2Bot):
    bot.add_cog(AdminSlashCommands(bot))
