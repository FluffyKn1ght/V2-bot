import asyncio
import time
import random
import io
from typing import NamedTuple

from cogs.v2cog import V2BotCog
from main import V2Bot

from disnake.ext import commands
from disnake.ext.commands import Param
from disnake import ApplicationCommandInteraction, File

from PIL import Image

# remember - we're running on a 40$ pancake computer qwq
MAX_JOBS_EVER = 1

PLANE_SIZE = (64, 64)

GIF_RESIZE_FACTOR = 3
GIF_THREAD_COUNT = 4  # MUST BE EVEN!!

MAX_ITERS_EVER = 1000

DIRS = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


class GameRules(NamedTuple):
    birth: list[int]
    survival: list[int]

    @staticmethod
    def from_string(s: str) -> GameRules:
        x = s.upper().split("/")

        if len(x) != 2 or x[0][0] != "B" or x[1][0] != "S":
            raise ValueError("bad rulestring")

        birth = []
        survival = []

        for n in x[0][1:]:
            birth.append(int(n))

        for n in x[1][1:]:
            survival.append(int(n))

        return GameRules(birth=birth, survival=survival)


class GameResults(NamedTuple):
    total_time: float
    avg_time: float
    history: list[list[bool]]


class ConwaysLifeSlashCommand(V2BotCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.jobs: set[int] = set()

    @commands.slash_command(
        name="conways_life",
        description="runs a conway's game of life simulation! (VERY SLOW)",
    )
    async def conways_life_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        cell_chance: float = Param(
            desc="chance for a cell to be born alive, 0.01-1.0. default is 0.5",
            ge=0.01,
            le=1.0,
            default=0.5,
        ),
        rulestring: str = Param(
            desc="rulestring for game. see wikipedia article. default: B3/S23",
            default="B3/S23",
        ),
    ):
        try:
            rules = GameRules.from_string(rulestring)
        except ValueError:
            await inter.response.send_message(
                "what is that rulestrihhhng vro :wilted_rose:", ephemeral=True
            )
            return

        if inter.user.id in self.jobs:
            await inter.response.send_message(
                "you already have a game running ya doofus", ephemeral=True
            )
            return

        if len(self.jobs) >= MAX_JOBS_EVER:
            await inter.response.send_message(
                "too many games running, sry im about to go :boom::boom::fire::fire::skull:",
                ephemeral=True,
            )
            return

        self.bot.log(
            f"(conways life) starting game with rulestring {rulestring} for user {inter.user.name} ({inter.user.id})"
        )
        self.jobs.add(inter.user.id)
        await inter.response.defer()

        results = await asyncio.to_thread(self.run_conways_life, cell_chance, rules)

        self.bot.log(
            f"(conways life) finished game for {inter.user.name} ({inter.user.id}), {len(results.history)-1} iters, took {results.total_time}s (avg time {results.avg_time}s, {(len(results.history)-1) / 60} iters/s)"
        )

        time1 = time.time()

        gif = await self.make_game_gif(results.history)

        # with open("testgif.webp", "wb") as fp:
        #     fp.write(gif.read())

        gif.seek(0)

        time2 = time.time()
        self.bot.log(
            f"(conways life) took {time2-time1}s to generate gif for {inter.user.id}"
        )

        await inter.edit_original_response(
            f"{len(results.history)-1} iters, took {round(results.total_time, 2)}s to run. ({round((len(results.history)-1) / 60, 2)} iters/s)",
            file=File(gif, filename="conways_life.webp"),
        )
        self.jobs.remove(inter.user.id)

    def run_conways_life(self, cell_chance: float, rules: GameRules):
        plane: list[bool] = [
            True if random.random() < cell_chance else False
            for _ in range(PLANE_SIZE[0] * PLANE_SIZE[1])
        ]

        iters = 0
        history = [plane] + [
            [False for _ in range(PLANE_SIZE[0] * PLANE_SIZE[1])]
            for _ in range(MAX_ITERS_EVER + 2)
        ]
        total_time = 0.0

        while iters < MAX_ITERS_EVER:
            diff = False

            plane2 = list(plane)

            time1 = time.time()

            idx = 0
            for cell in plane:
                x = int(idx % PLANE_SIZE[0])
                y = int(idx // PLANE_SIZE[0])

                neighbours = 0
                for dir in DIRS:
                    nx = x + dir[0]
                    ny = y + dir[1]
                    nidx = nx + (ny * PLANE_SIZE[0])

                    try:
                        if plane[nidx]:
                            neighbours += 1
                    except IndexError:
                        pass

                if not plane[idx] and neighbours in rules.birth:
                    plane2[idx] = True
                    diff = True
                elif not neighbours in rules.survival:
                    plane2[idx] = False
                    diff = True

                idx += 1

            history[iters + 1] = plane2
            iters += 1

            plane = plane2

            if not diff:
                break

            total_time += time.time() - time1

        return GameResults(
            avg_time=total_time / iters,
            total_time=total_time,
            history=history[: iters + 1],
        )

    async def make_game_gif(self, history: list[list[bool]]) -> io.BytesIO:
        # this is SUCH A HACK but it's 4:48am rn so idfc
        while len(history) % GIF_THREAD_COUNT:
            history.append(history[-1])
        chunk_size = len(history) // GIF_THREAD_COUNT
        tasks = [
            asyncio.to_thread(self._make_game_frames, history[i : i + chunk_size])
            for i in range(0, len(history), chunk_size)
        ]

        frame_chunks = await asyncio.gather(*tasks)

        frames = []
        for frame_chunk in frame_chunks:
            frames += frame_chunk

        gif = io.BytesIO()
        frames[0].save(
            gif,
            format="WEBP",
            append_images=frames[1:],
            duration=175,
            optimize=True,
            save_all=True,
        )

        # remember to rewind ur vhs tapes kids!!
        gif.seek(0)

        return gif

    def _make_game_frames(self, history_chunk: list[list[bool]]) -> list[Image.Image]:
        frames = []

        for plane in history_chunk:
            frame = Image.new("RGB", size=(PLANE_SIZE[0], PLANE_SIZE[1]))
            pixels = frame.load()
            for y in range(PLANE_SIZE[1]):
                for x in range(PLANE_SIZE[0]):
                    pixels[x, y] = (  # type: ignore
                        (0, 0, 0) if plane[x + (y * PLANE_SIZE[0])] else (255, 255, 255)
                    )

            frame = frame.resize(
                (PLANE_SIZE[0] * GIF_RESIZE_FACTOR, PLANE_SIZE[1] * GIF_RESIZE_FACTOR),
                resample=Image.Resampling.NEAREST,
            )
            frames.append(frame)

        return frames


def setup(bot: V2Bot):
    bot.add_cog(ConwaysLifeSlashCommand(bot))
