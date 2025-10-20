import pygame as pg

import thehand as th


class AudioVisualizer(th.Entity):
    def __init__(
        self,
        pos: tuple[int, int],
        store: th.Store,
    ) -> None:
        self.pos = pos
        self.store = store

        self.audio_icon = pg.image.load(th.asset_path("imgs", "wave.png")).convert_alpha()
        self.audio_icon = pg.transform.scale2x(self.audio_icon)
        self.audio_icon_rect = self.audio_icon.get_rect(center=pos)

        self.speech = ""

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self) -> None:
        self.store.screen.blit(self.audio_icon, self.audio_icon_rect)

        speech_text = self.store.font_text_24.render(self.speech[-32:], True, th.COLOR_MOCHA_TEXT)
        speech_text_rect = speech_text.get_rect(
            center=(self.pos[0], self.pos[1] + self.audio_icon_rect.height // 2 + 48)
        )
        self.store.screen.blit(speech_text, speech_text_rect)
