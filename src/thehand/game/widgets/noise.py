import thehand as th


class Noise(th.Entity):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        pos: tuple[int, int] = (50, 50),
        color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
    ) -> None:
        super().__init__(state, store)

        self.pos = pos
        self.color = color

        self.text = ""
        self.step = 500
        self._last_update = 0

    def setup(self) -> None:
        return

    def handle_events(self) -> None:
        return

    def update(self) -> None:
        if self.state.now - self.step > self._last_update:
            self._last_update = self.state.now
            self.text = th.generate_noise_string()

    def render(self) -> None:
        text_sur = self.store.font_pixel_24.render(self.text, True, self.color)
        text_rect = text_sur.get_rect(center=self.pos)
        self.store.screen.blit(text_sur, text_rect)
