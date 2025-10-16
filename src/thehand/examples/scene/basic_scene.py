import pygame

from thehand.core import Scene, State
from thehand.core.event import create_next_scene_event


class BasicScene(Scene):
    def cleanup(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.event.post(create_next_scene_event(f"Request from {self.name}"))

    def update(self):
        self.gray = min(self.gray + 0.5, 255)

    def render(self):
        color = int(self.gray)
        self.screen.fill((color, color, color))
        pygame.display.flip()

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
