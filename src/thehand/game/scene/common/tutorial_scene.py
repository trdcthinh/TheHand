import pygame as pg

from thehand.core import State, asset_path
from thehand.core.types import StoryChunk
from thehand.game.scene.common.story_scene import StoryScene


class TutorialScene(StoryScene):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ):
        chunks: list[StoryChunk] = [
            {
                "name": "00_00",
                "image": pg.image.load(asset_path("imgs/tutorial_00_00.jpg")),
                "sound": "vine_boom",
                "text": "Welcome to The Hand! The game where you use your body to play.",
                "duration": 5000,
            },
            {
                "name": "00_01",
                "image": pg.image.load(asset_path("imgs/tutorial_00_01.jpg")),
                "sound": "auughhh",
                "text": "Use your hands, face, and body to control the game.",
                "duration": 5000,
            },
            {
                "name": "00_02",
                "image": pg.image.load(asset_path("imgs/tutorial_00_02.jpg")),
                "sound": "error",
                "text": "And your voice to issue commands.",
                "duration": 5000,
            },
            {
                "name": "01_00",
                "image": pg.image.load(asset_path("imgs/tutorial_01_00.jpg")),
                "sound": "vine_boom",
                "text": "This is the hand landmark detection.",
                "duration": 5000,
            },
            {
                "name": "01_01",
                "image": pg.image.load(asset_path("imgs/tutorial_01_01.jpg")),
                "sound": "auughhh",
                "text": "It tracks your hand movements.",
                "duration": 5000,
            },
            {
                "name": "01_02",
                "image": pg.image.load(asset_path("imgs/tutorial_01_02.jpg")),
                "sound": "error",
                "text": "You can use it to move the cursor.",
                "duration": 5000,
            },
            {
                "name": "01_04",
                "image": pg.image.load(asset_path("imgs/tutorial_01_04.jpg")),
                "sound": "vine_boom",
                "text": "Or interact with objects.",
                "duration": 5000,
            },
            {
                "name": "02_00",
                "image": pg.image.load(asset_path("imgs/tutorial_02_00.jpg")),
                "sound": "auughhh",
                "text": "This is the pose landmark detection.",
                "duration": 5000,
            },
            {
                "name": "02_01",
                "image": pg.image.load(asset_path("imgs/tutorial_02_01.jpg")),
                "sound": "error",
                "text": "It tracks your body movements.",
                "duration": 5000,
            },
            {
                "name": "02_02",
                "image": pg.image.load(asset_path("imgs/tutorial_02_02.jpg")),
                "sound": "vine_boom",
                "text": "You can use it to control your character.",
                "duration": 5000,
            },
        ]
        super().__init__(name, screen, state, chunks)
