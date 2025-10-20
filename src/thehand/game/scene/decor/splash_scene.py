import pygame as pg

from thehand.core import Scene, State, Store, asset_path


class SplashScene(Scene):
    def __init__(
        self,
        name: str,
        state: State,
        store: Store,
        icon_ratio: float = 0.3,
    ):
        super().__init__(name, state, store)

        self.image = None
        self.image_rect = None

        self.icon_ratio = icon_ratio

        self.alpha = 0
        self.scale = 0.8
        self.animation_speed = 2
        self.zoom_speed = 0.005

        self.duration = 3500
        self.start_time = pg.time.get_ticks()

    def setup(self):
        original_image = pg.image.load(
            asset_path("imgs", "thehand_icon.png")
        ).convert_alpha()
        new_height = self.store.screen.get_height() * self.icon_ratio
        aspect_ratio = original_image.get_width() / original_image.get_height()
        new_width = new_height * aspect_ratio
        self.image = pg.transform.smoothscale(original_image, (new_width, new_height))
        self.image_rect = self.image.get_rect(
            center=self.store.screen.get_rect().center
        )

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def update(self):
        if self.alpha < 255:
            self.alpha += self.animation_speed
            self.alpha = min(self.alpha, 255)

        if self.scale < 1.0:
            self.scale += self.zoom_speed
            self.scale = min(self.scale, 1.0)

        if pg.time.get_ticks() - self.start_time > self.duration:
            self.done = True

    def render(self):
        self.store.screen.fill((25, 25, 25))

        if self.image:
            scaled_image = pg.transform.smoothscale_by(self.image, self.scale)
            scaled_image.set_alpha(self.alpha)
            scaled_rect = scaled_image.get_rect(center=self.image_rect.center)
            self.store.screen.blit(scaled_image, scaled_rect)

        pg.display.flip()
