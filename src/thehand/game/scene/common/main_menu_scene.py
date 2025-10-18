import pygame as pg

from thehand.core import HandLandmarker, Scene, SpeechRecognition, State
from thehand.core.event import create_next_scene_event
from thehand.examples.callback import dislike_quit_callback, sr_next_scene_callback


class MainMenuScene(Scene):
    def sr_callback(self, text: str):
        self.display_text = text
        sr_next_scene_callback(text)

    def setup(self):
        self.sr.set_result_callback(self.sr_callback)
        self.hand.set_result_callback(dislike_quit_callback)

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pg.event.post(create_next_scene_event())

    def update(self):
        return

    def render(self):
        self.screen.fill((0, 0, 0))
        text_sur = self.font.render(f'"{self.display_text}"', True, (255, 255, 255))
        self.screen.blit(text_sur, (100, 100))
        pg.display.flip()

    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
        sr: SpeechRecognition,
    ):
        super().__init__(name, screen, state)

        self.sr = sr

        self.font = pg.font.SysFont("Comic Sans MS", 32)

        self.display_text = ""
