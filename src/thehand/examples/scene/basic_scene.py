import pygame
from thehand.core import Scene, State


class BasicScene(Scene):
    def cleanup(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("next")
        pass

    def update(self):
        self.gray = min(self.gray + 0.5, 255)
        pass

    def render(self):
        color = int(self.gray)
        self.screen.fill((color, color, color))
        pygame.display.flip()
        pass

    def setup(self) -> None:
        pass

    def __init__(
        self,
        name: str,
        screen: pygame.Surface,
        state: State,
    ):
        super().__init__(name, screen, state)

        self.gray = 0
