import io
import asyncio

from main import V2Bot
from cogs.v2cog import V2BotCog

from disnake import ApplicationCommandInteraction, File, Attachment
from disnake.ext import commands
from disnake.ext.commands import Param

from PIL import Image, UnidentifiedImageError

FRAME_X, FRAME_Y, FRAME_W, FRAME_H = 90, 90, 836, 580

class FrameSlashCommand(V2BotCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.frame = Image.open("./medihha/frame.png")
        
    @commands.slash_command(name="frame", description="frames an image like a work of art! (no gifs)")
    async def frame_slash_command(
        self, 
        inter: ApplicationCommandInteraction, 
        imgfile: Attachment = Param(
            desc="the image to frame (otherwise selected msg)",
            default=None
        ),
    ):
        await inter.response.defer(ephemeral=True)
    
        imgdata: bytes = b""
        
        if imgfile:
            if imgfile.content_type.split("/")[0] == "image":
                try:
                    imgdata = await imgfile.read()
                except UnidentifiedImageError, OSError, IOError:
                    await inter.edit_original_response("what is this image vro :wilted_rose:")
        else:
            if inter.user.id in self.bot.selected_messages:
                try:
                    msg = await inter.channel.fetch_message(self.bot.selected_messages[inter.user.id])
                except Exception as e:
                    await inter.edit_original_response("your selected message is in a different channel or no longer exists")
                    return
                
                for attachment in msg.attachments:
                    if attachment.content_type.split("/")[0] == "image":
                        try:
                            imgdata = await attachment.read()
                        except UnidentifiedImageError, OSError, IOError:
                            continue
                        
                        break
        
        if not imgdata:
            await inter.edit_original_response("add an image via the imgfile parameter or choose a message")
            return
        
        result: Image = await asyncio.to_thread(self.frame_image, Image.open(io.BytesIO(imgdata)))
        
        result_file = io.BytesIO()
        result.save(result_file, format="PNG")
        result_file.seek(0)
        
        await inter.channel.send(file=File(result_file, filename="framed.png"))
        
        await inter.delete_original_response()

    def frame_image(self, img: Image) -> Image:
        img = img.resize((FRAME_W, FRAME_H))
        
        img2 = Image.new(mode="RGBA", size=self.frame.size)
        img2.paste(img, (FRAME_X, FRAME_Y))
        img2.paste(self.frame, (0, 0), self.frame)
        
        return img2
        
def setup(bot: V2Bot):
    bot.add_cog(FrameSlashCommand(bot))
