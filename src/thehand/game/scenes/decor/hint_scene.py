import thehand as th


<<<<<<< HEAD:src/thehand/game/scene/decor/hint_scene.py
class HintScene(Scene):
    def __init__(
        self,
        name: str,
        state: State,
        store: Store,
        background_path: str | None = None,
        hint_text: str = "HINT",
        text_color: tuple[int, int, int] = (240, 240, 240),
    ):
=======
class HintScene(th.Scene):
    def __init__(self, name: str, state: th.State, store: th.Store):
>>>>>>> 2e70353244bc5f403f626c6aec789fe818477d33:src/thehand/game/scenes/decor/hint_scene.py
        super().__init__(name, state, store)
        self.background_path = background_path
        self.hint_text = hint_text
        self.text_color = text_color

        self.background = None  # Surface

    def setup(self):
        """Khởi tạo ảnh nền (nếu có)."""
        if self.background_path:
            try:
                self.background = pg.image.load(self.background_path).convert()
                self.background = pg.transform.scale(
                    self.background,
                    self.store.screen.get_size(),
                )
            except Exception as e:
                print(f"[HintScene] Không thể tải background: {e}")
                self.background = None

        self.have_setup = True

    def handle_events(self):
        """Xử lý sự kiện — tạm thời chỉ cho thoát bằng ESC."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.done = True

    def update(self):
        """Không cần cập nhật gì trong scene tĩnh."""
        pass

    def render(self):
<<<<<<< HEAD:src/thehand/game/scene/decor/hint_scene.py
        screen = self.store.screen
        screen.fill((25, 25, 25))

        # vẽ background nếu có
        if self.background:
            screen.blit(self.background, (0, 0))

        # vẽ dòng chữ ở góc dưới
        font = self.store.font_text_24
        text_surface = font.render(self.hint_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (
            10,
            screen.get_height() - 10,
        )
        screen.blit(text_surface, text_rect)

        pg.display.flip()
=======
        self.store.screen.fill((25, 25, 25))
        text = self.store.font_text_24.render(self.name, True, (240, 240, 240))
        self.store.screen.blit(text, (100, 100))
>>>>>>> 2e70353244bc5f403f626c6aec789fe818477d33:src/thehand/game/scenes/decor/hint_scene.py
