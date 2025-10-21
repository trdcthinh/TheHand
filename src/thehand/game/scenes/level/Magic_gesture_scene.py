import pygame as pg

import thehand as th


class MagicGestureScene(th.Scene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        # Match Scene signature: (state, store, name)
        super().__init__(state, store, name)

        # Screen: prefer store.screen if available, else create a temporary surface
        if getattr(self.store, "screen", None):
            self.screen = self.store.screen
        else:
            self.screen = pg.display.get_surface() or pg.Surface(self.state.window_size)

        # Light-weight background: try to load, otherwise solid fill
        bg_path = th.asset_path("imgs", "mgs_background.jpg")
        try:
            self.bg_img = pg.image.load(bg_path).convert()
            self.bg_img = pg.transform.scale(self.bg_img, self.screen.get_size())
        except Exception:
            # Keep a very lightweight fallback
            self.bg_img = pg.Surface(self.screen.get_size())
            self.bg_img.fill((30, 30, 46))  # dark base fallback

        # Choose ground Y simply near bottom to avoid heavy pixel scans
        self.ground_y = self.screen.get_height() - int(self.screen.get_height() * 0.05)

        # Load main character (light processing): use colorkey for transparency if needed
        char_path = th.asset_path("imgs", "mgs_main_character.png")
        try:
            char_img = pg.image.load(char_path).convert_alpha()
            # Remove near-black pixels (rgb <5) by setting alpha=0 where supported.
            # This is faster than per-pixel blits for moderate-sized images.
            try:
                arr = pg.surfarray.pixels3d(char_img)
                alpha = pg.surfarray.pixels_alpha(char_img)
                mask = (arr[:, :, 0] < 5) & (arr[:, :, 1] < 5) & (arr[:, :, 2] < 5)
                alpha[mask] = 0
                del arr, alpha
            except Exception:
                # Fallback to colorkey if surfarray access isn't available
                try:
                    char_img.set_colorkey((0, 0, 0))
                except Exception:
                    pass

            char_w = int(self.screen.get_width() * 0.10)
            scale_h = int(char_img.get_height() * (char_w / max(1, char_img.get_width())))
            self.char_img = pg.transform.smoothscale(char_img, (char_w, scale_h))
            self.char_rect = self.char_img.get_rect()
            self.char_rect.centerx = self.screen.get_width() // 2
            self.char_rect.bottom = self.ground_y - (self.char_img.get_height() * 0.65)
        except Exception:
            # Minimal fallback (small square)
            self.char_img = pg.Surface((50, 50), pg.SRCALPHA)
            self.char_img.fill((255, 0, 0, 180))
            self.char_rect = self.char_img.get_rect(centerx=self.screen.get_width() // 2, bottom=self.ground_y)

        # Running flag for test harness
        self.done = False

    def setup(self) -> None:
        # no heavy setup required
        return None

    def handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.QUIT:
                self.done = True

    def update(self) -> None:
        # lightweight update placeholder (no heavy computations)
        return None

    def render(self) -> None:
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.char_img, self.char_rect)
        # keep flip so the example/test shows output when run standalone
        pg.display.flip()
