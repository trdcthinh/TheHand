import pygame as pg

from thehand.core import Scene, State, asset_path


class TutorialScene(Scene):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ):
        super().__init__(name, screen, state)

        self.chunks = [
            {
                "image": pg.image.load(asset_path("imgs/tutorial_00_00.jpg")),
                "sound": "vine_boom",
                "text": "Welcome to The Hand! The game where you use your body to play.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_00_01.jpg")),
                "sound": "auughhh",
                "text": "Use your hands, face, and body to control the game.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_00_02.jpg")),
                "sound": "error",
                "text": "And your voice to issue commands.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_01_00.jpg")),
                "sound": "vine_boom",
                "text": "This is the hand landmark detection.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_01_01.jpg")),
                "sound": "auughhh",
                "text": "It tracks your hand movements.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_01_02.jpg")),
                "sound": "error",
                "text": "You can use it to move the cursor.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_01_04.jpg")),
                "sound": "vine_boom",
                "text": "Or interact with objects.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_02_00.jpg")),
                "sound": "auughhh",
                "text": "This is the pose landmark detection.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_02_01.jpg")),
                "sound": "error",
                "text": "It tracks your body movements.",
                "duration": 5000,
            },
            {
                "image": pg.image.load(asset_path("imgs/tutorial_02_02.jpg")),
                "sound": "vine_boom",
                "text": "You can use it to control your character.",
                "duration": 5000,
            },
        ]
        self.current_chunk_index = 0
        self.chunk_timer = 0

    def setup(self):
        self.chunk_timer = pg.time.get_ticks()
        sound_name = self.chunks[self.current_chunk_index]["sound"]
        if sound_name in self.state.sounds:
            pg.mixer.Sound.play(self.state.sounds[sound_name])

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if (
                    event.key == pg.K_ESCAPE
                    or event.key == pg.K_SPACE
                    or event.key == pg.K_KP_ENTER
                ):
                    self.done = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.done = True

    def update(self):
        now = pg.time.get_ticks()
        if now - self.chunk_timer > self.chunks[self.current_chunk_index]["duration"]:
            self.current_chunk_index += 1
            if self.current_chunk_index >= len(self.chunks):
                self.done = True
            else:
                self.chunk_timer = now
                sound_name = self.chunks[self.current_chunk_index]["sound"]
                if sound_name in self.state.sounds:
                    self.state.sounds[sound_name].play()

    def render(self):
        if self.done:
            return

        chunk = self.chunks[self.current_chunk_index]

        bg_image = pg.transform.scale(chunk["image"], self.screen.get_size())
        self.screen.blit(bg_image, (0, 0))

        text_surface = self.state.text_font_lg.render(
            chunk["text"], True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(
            center=(self.state.window_size[0] // 2, self.state.window_size[1] - 100)
        )
        self.screen.blit(text_surface, text_rect)

        pg.display.flip()
