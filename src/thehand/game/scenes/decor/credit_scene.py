import thehand as th


class CreditScene(th.Scene):
    def __init__(self, name: str, state: th.State, store: th.Store):
        super().__init__(name, state, store)

    def setup(self):
        # Màu nền và chữ
        self.bg_color = (20, 20, 20)
        self.text_color = (255, 255, 255)

        # Dòng chữ cảm ơn
        self.lines = [
            "CREDITS",
            "",
            "Thiết kế & Lập trình: Đội phát triển TheHand",
            "Developed by:",
            "  - Nguyễn Thế Anh",
            "  - Trần Đức Thịnh",
            "  - Châm Duy Khoát",
            "  - Hoàng Minh Nhất",
            "  - Đinh Duy Khương",
            "",
            "",
            "Đặc biệt cảm ơn bạn đã trải nghiệm trò chơi!",
            "",
            "Nhấn ESC hoặc SPACE để thoát."
        ]

        self.have_setup = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_SPACE):
                    self.done = True

    def update(self):
        # Có thể thêm hiệu ứng di chuyển chữ hoặc nhạc nền nếu muốn
        pass

    def render(self):
<<<<<<< HEAD:src/thehand/game/scene/decor/credit_scene.py
        self.store.screen.fill(self.bg_color)

        # Vẽ từng dòng chữ
        y = 150
        for line in self.lines:
            text_surface = self.store.font_text_24.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.store.screen.get_width() / 2, y))
            self.store.screen.blit(text_surface, text_rect)
            y += 40

        pg.display.flip()
=======
        self.store.screen.fill((25, 25, 25))
        text = self.store.font_text_24.render(self.name, True, (240, 240, 240))
        self.store.screen.blit(text, (100, 100))
>>>>>>> 2e70353244bc5f403f626c6aec789fe818477d33:src/thehand/game/scenes/decor/credit_scene.py
