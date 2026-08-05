import io
import math
import random
import wave

from disnake.ext import commands
from disnake.file import File
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot

MIN_AUDIO_LENGTH = 0.5
MAX_AUDIO_LENGTH = 1.5


class GETOUSlashCommand(V2BotCog):
    @commands.slash_command(name="getou", description="GETOU-")
    async def getou_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()

        wav = wave.open("./medihha/getout.wav", "r")

        length_secs = wav.getnframes() / wav.getframerate()

        new_length = min(
            max(random.random() * length_secs, MIN_AUDIO_LENGTH), MAX_AUDIO_LENGTH
        )

        new_length_frames = math.floor(new_length * wav.getframerate())

        wav2_buffer = io.BytesIO()
        wav2 = wave.open(wav2_buffer, "wb")
        wav2.setframerate(wav.getframerate())
        wav2.setnchannels(wav.getnchannels())
        wav2.setnframes(new_length_frames)
        wav2.setsampwidth(wav.getsampwidth())
        wav2.writeframes(wav.readframes(new_length_frames))

        wav.close()
        wav2.close()

        wav2_buffer.seek(0)

        await inter.edit_original_response(file=File(wav2_buffer, filename="getou.wav"))


def setup(bot: V2Bot):
    bot.add_cog(GETOUSlashCommand(bot))
