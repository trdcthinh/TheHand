import pygame as pg
import os
import numpy as np
from thehand.core import Scene, State, Store, asset_path

class MagicGestureScene(Scene):
    def __init__(self, name: str, state: State, store: Store, screen: pg.Surface):
        super().__init__(name, state, store)
        self.screen = screen  # Store the screen surface
        # Load background
        bg_path = asset_path("imgs", "mgs_background.jpg")
        try:
            self.bg_img = pg.image.load(bg_path).convert()
            self.bg_img = pg.transform.scale(self.bg_img, self.screen.get_size())
            print(f"[DEBUG] Background image loaded: {bg_path}")
        except pg.error as e:
            print(f"[ERROR] Error loading background image {bg_path}: {e}")
            self.bg_img = pg.Surface(self.screen.get_size())
            self.bg_img.fill((0, 0, 0)) # Fallback to black background

        # Find ground y position (pixel đầu tiên từ trên xuống có màu rgba(150,203,87))
        ground_y = None
        if self.bg_img:
            bg_array = pg.surfarray.pixels3d(self.bg_img)
            w, h = self.screen.get_size()
            for y in range(h):
                for x in range(w):
                    r, g, b = bg_array[x, y]
                    if (r, g, b) == (150, 203, 87):
                        ground_y = y
                        break
                if ground_y is not None:
                    break
        if ground_y is None:
            ground_y = self.screen.get_height() - 1  # fallback
        print(f"[DEBUG] Ground Y position found: {ground_y}")

        # Load and process main character
        char_path = asset_path("imgs", "mgs_main_character.png")
        try:
            char_img = pg.image.load(char_path).convert_alpha()
            print(f"[DEBUG] Character image loaded: {char_path}")
            # Remove black pixels (rgba <3, <3, <3)
            arr = pg.surfarray.pixels3d(char_img)
            alpha = pg.surfarray.pixels_alpha(char_img)
            mask = (arr[:,:,0] < 5) & (arr[:,:,1] < 5) & (arr[:,:,2] < 5)
            alpha[mask] = 0
            del arr, alpha
            # Resize character
            char_w = int(self.screen.get_width() * 0.1)
            char_h = int(char_img.get_height() * (char_w / char_img.get_width()))
            self.char_img = pg.transform.smoothscale(char_img, (char_w, char_h))
            # Tính vị trí vẽ nhân vật
            char_rect = self.char_img.get_rect()
            char_rect.centerx = self.screen.get_width() // 2
            char_rect.bottom = ground_y
            self.char_rect = char_rect
            print(f"[DEBUG] Character position: {self.char_rect}")
        except pg.error as e:
            print(f"[ERROR] Error loading character image {char_path}: {e}")
            self.char_img = pg.Surface((50, 50), pg.SRCALPHA)
            self.char_img.fill((255, 0, 0, 128)) # Fallback to red square
            self.char_rect = self.char_img.get_rect(centerx=self.screen.get_width() // 2, bottom=ground_y)

    def setup(self):
        pass

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.char_img, self.char_rect)
        pg.display.flip()