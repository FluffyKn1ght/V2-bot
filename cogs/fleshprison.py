import asyncio

from disnake import ApplicationCommandInteraction, Member
from disnake.ext import commands
from disnake.ext.commands.cog import Cog
from disnake.member import Member
from disnake.message import Message
from disnake.role import Role

from cogs.v2cog import V2BotCog
from main import V2Bot


class FleshPrison(V2BotCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.allow_unflesh: set[int] = set()

    @Cog.listener("on_message")
    async def do_fleshprison_thingy(self, msg: Message):
        self.allow_unflesh.discard(msg.author.id)
    
        if not self.bot.can_j_in_channel(msg.channel.id):
            return
    
        for role_id in self.bot.config["horny"].keys():
            role_id = int(role_id)
            for role in msg.author.roles:  # type: ignore
                if role.id == role_id:
                    if not msg.channel.id in self.bot.config["horny"][str(role_id)]:
                        await msg.delete()

                continue

    @Cog.listener("on_member_update")
    async def curse_of_binding(self, before: Member, after: Member):
        if before.id in self.allow_unflesh:
            return
    
        for role_id in self.bot.config["horny"].keys():
            try:
                role = await after.guild.fetch_role(role_id)
            except Exception:
                continue

            if role in before.roles and not role in after.roles:
                await after.add_roles(role, reason="STAY IN THE BOX")
    
    @commands.slash_command(name="unflesh", description="releases someone from flesh prison")
    async def unflesh_slash_command(self, inter: ApplicationCommandInteraction, target: Member):
        is_mod = False
        for role in inter.user.roles:
            if role.id in self.bot.config["horny_guards"]:
                is_mod = True
                break
                
        if not is_mod:
            await inter.response.send_message("who do you think you are?", ephemeral=True)
            return
        
        if target.id == inter.user.id:
            await inter.response.send_message("do you think you're above the law?", ephemeral=True)
            return
        
        for role_id in self.bot.config["horny"]:
            try:
                role = await inter.guild.fetch_role(role_id)
            except Exception:
                continue
            
            self.allow_unflesh.add(target.id)
            
            await target.remove_roles(role)
        
        await inter.response.send_message(":+1:", ephemeral=True)
        
        await asyncio.sleep(5) # hacky hack
        
        self.allow_unflesh.discard(target.id)
        

def setup(bot: V2Bot):
    bot.add_cog(FleshPrison(bot))
