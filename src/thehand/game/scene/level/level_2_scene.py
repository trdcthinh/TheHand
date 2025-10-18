import pygame as pg

from thehand.core import HandLandmarker, Scene, SpeechRecognition, State
from thehand.core.event import create_next_scene_event
from thehand.examples.callback import count_hand_callback, sr_close_callback


class Level02Scene(Scene):
    def sr_result_callback(self, text: str) -> None:
        sr_close_callback(text)

    def setup(self):
        self.sr.set_result_callback(sr_close_callback)
        self.hand.set_result_callback(count_hand_callback)

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pg.event.post(create_next_scene_event())

    def update(self):
        return

    def render(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render('"Nice to meet you."', True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        pg.display.flip()

    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
        sr: SpeechRecognition,
        hand: HandLandmarker,
    ):
        super().__init__(name, screen, state)

        self.sr = sr
        self.hand = hand

        self.font = pg.font.SysFont("Comic Sans MS", 32)
