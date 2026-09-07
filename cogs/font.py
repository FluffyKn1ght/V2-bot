import asyncio

from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Param

from cogs.v2cog import V2BotCog
from main import V2Bot

#NORMAL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
#SCRIPT_LETTERS = "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
SCRIPT_LETTERS = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
GOTHIC_LETTERS = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"

class FontSlashCommand(V2BotCog):
    @commands.slash_command(name="font", description="makes your font 𝓮𝔁𝓺𝓾𝓲𝓼𝓲𝓽𝓮")
    async def font_slash_command(
        self, 
        inter: ApplicationCommandInteraction, 
        text: str = Param(desc="the text to change the font of"), 
        font: str = Param(
            desc="which font to use",
            choices={
                "𝓢𝓬𝓻𝓲𝓹𝓽": "script",
                "𝕲𝖔𝖙𝖍𝖎𝖈": "gothic" # goth femboys
            },
            default="script"
        )
    ):
        await inter.response.defer(ephemeral=True)
    
        if font == "script":
            font_chars = SCRIPT_LETTERS
        elif font == "gothic":
            font_chars = GOTHIC_LETTERS
    
        if len(text) >= 512:
            text2 = await asyncio.to_thread(FontSlashCommand.replace_font, text, font_chars)
        else:
            text2 = FontSlashCommand.replace_font(text, font_chars)
        
        await inter.edit_original_response(text2[:2000])
        
            
        
    @staticmethod
    def replace_font(text: str, font: str) -> str:
        s = ""
        for char in text:
            id = ord(char)
            if id >= 65 and id <= 90: # A-Z
                adj = 65
            elif id >= 97 and id <= 122: # a-z
                adj = 97 - 26 # hiooooo
            else:
                s += char
                continue
        
            s += font[id - adj]
        
        return s

def setup(bot: V2Bot):
    bot.add_cog(FontSlashCommand(bot))
