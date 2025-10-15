import pygame

from thehand.core.scene import Scene


class OpeningScene(Scene):
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
