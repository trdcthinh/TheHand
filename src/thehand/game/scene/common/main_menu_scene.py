import pygame as pg

from thehand.core import Scene, State


class MainMenuScene(Scene):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ):
        super().__init__(name, screen, state)
        import os

        from thehand.core import asset_path

        self.caption = "No KEYBOARD No MOUSE"
        # Load GIF frames
        self.bg_frames = []
        self.bg_frame_idx = 0
        self.bg_frame_timer = 0
        self.bg_frame_delay = 100  # ms per frame
        try:
            import PIL.Image

            gif_path = asset_path(os.path.join("imgs", "menu_background.gif"))
            pil_img = PIL.Image.open(gif_path)
            for frame in range(0, pil_img.n_frames):
                pil_img.seek(frame)
                frame_img = pil_img.convert("RGBA")
                raw_str = frame_img.tobytes()
                size = frame_img.size
                pg_img = pg.image.frombytes(raw_str, size, "RGBA")
                self.bg_frames.append(pg_img)
        except Exception:
            self.bg_frames = []
        # Button setup
        self.button_font = pg.font.Font("data/fonts/PixeloidSansBold.ttf", 36)
        self.start_btn_rect = pg.Rect(0, 0, 260, 70)
        self.quit_btn_rect = pg.Rect(0, 0, 260, 70)
        w, h = self.screen.get_size()
        self.start_btn_rect.center = (w // 2, h // 2 + 60)
        self.quit_btn_rect.center = (w // 2, h // 2 + 150)
        # Button effect state
        self.active_btn = None  # 'start' or 'quit'
        self.active_btn_time = 0
        # Speech recognition
        from thehand.core.audition.speech_recognition import SpeechRecognition

        self.last_spoken = ""
        self.sr_running = False
        self.sr = SpeechRecognition(state, self._on_speech)

    def setup(self):
        pg.display.set_caption(self.caption)
        if not self.sr_running:
            import threading

            self.sr_running = True
            threading.Thread(target=self.sr.run, daemon=True).start()

    # Nói Quit để thoát game
    def _on_speech(self, text):
        if text:
            self.last_spoken = text
            t = text.lower()
            if "quit" in t:
                self._activate_button("quit")
                self._delayed_done()
            elif "start" in t:
                self._activate_button("start")
                self.next_scene = "tutorial"
                self._delayed_done()

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.QUIT:
                self._activate_button("quit")
                self._delayed_done()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.start_btn_rect.collidepoint(mx, my):
                    self._activate_button("start")
                    self.next_scene = "tutorial"
                    self._delayed_done()
                elif self.quit_btn_rect.collidepoint(mx, my):
                    self._activate_button("quit")
                    self._delayed_done()

    def _delayed_done(self):
        import threading

        def set_done():
            import time

            time.sleep(1.5)
            self.done = True

        threading.Thread(target=set_done, daemon=True).start()

    def update(self):
        now = pg.time.get_ticks()
        if self.bg_frames:
            if now - self.bg_frame_timer > self.bg_frame_delay:
                self.bg_frame_idx = (self.bg_frame_idx + 1) % len(self.bg_frames)
                self.bg_frame_timer = now
        # Reset button effect after 0.5s
        if self.active_btn and now - self.active_btn_time > 500:
            self.active_btn = None

    def render(self):
        # Draw animated background
        if self.bg_frames:
            bg = pg.transform.scale(
                self.bg_frames[self.bg_frame_idx], self.screen.get_size()
            )
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill((25, 25, 25))
        # Draw Start button
        self._draw_button(
            self.start_btn_rect, "START", active=(self.active_btn == "start")
        )
        # Draw Quit button
        self._draw_button(
            self.quit_btn_rect, "QUIT", active=(self.active_btn == "quit")
        )
        # Draw last spoken text as subtitle
        if self.last_spoken:
            subtitle_font = pg.font.Font("data/fonts/SpaceMono.ttf", 32)
            subtitle_surf = subtitle_font.render(self.last_spoken, True, (255, 255, 0))
            subtitle_rect = subtitle_surf.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() - 60)
            )
            self.screen.blit(subtitle_surf, subtitle_rect)
        pg.display.flip()

    def _draw_button(self, rect, text, active=False):
        # Button colors
        bg_color = (144, 238, 144)
        border_color = (0, 0, 0)
        txt_color = (0, 0, 0)
        if active:
            bg_color, border_color, txt_color = border_color, bg_color, (144, 238, 144)
            rect = rect.copy()
            rect.y += 5  # lún xuống 5px
        pg.draw.rect(self.screen, bg_color, rect)
        pg.draw.rect(self.screen, border_color, rect, 4)
        txt_surf = self.button_font.render(text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)

    def _activate_button(self, btn_name):
        self.active_btn = btn_name
        self.active_btn_time = pg.time.get_ticks()
