import pygame as pg

from thehand.core import Scene, State
from thehand.core.types import StoryChunk


class StoryScene(Scene):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
        chunks: list[StoryChunk],
    ):
        super().__init__(name, screen, state)

        self.chunks = chunks
        self.current_chunk_index = 0
        self.chunk_timer = 0

    def setup(self):
        self.current_chunk_index = 0
        self.chunk_timer = pg.time.get_ticks()
        chunk = self.chunks[self.current_chunk_index]
        if "sound" in chunk and chunk["sound"] in self.state.sounds:
            pg.mixer.Sound.play(self.state.sounds[chunk["sound"]])

    def handle_events(self):
        return

    def update(self):
        now = pg.time.get_ticks()
        if "duration" in self.chunks[self.current_chunk_index]:
            if (
                now - self.chunk_timer
                > self.chunks[self.current_chunk_index]["duration"]
            ):
                self.current_chunk_index += 1
                if self.current_chunk_index >= len(self.chunks):
                    self.done = True
                else:
                    self.chunk_timer = now
                    chunk = self.chunks[self.current_chunk_index]
                    if "sound" in chunk and chunk["sound"] in self.state.sounds:
                        self.state.sounds[chunk["sound"]].play()

    def render(self):
        if self.done:
            return

        chunk = self.chunks[self.current_chunk_index]

        if "image" in chunk:
            bg_image = pg.transform.scale(chunk["image"], self.screen.get_size())
            self.screen.blit(bg_image, (0, 0))

        if "text" in chunk:
            text_surface = self.state.text_font_lg.render(
                chunk["text"], True, (255, 255, 255)
            )
            text_rect = text_surface.get_rect(
                center=(self.state.window_size[0] // 2, self.state.window_size[1] - 100)
            )
            self.screen.blit(text_surface, text_rect)

        pg.display.flip()
