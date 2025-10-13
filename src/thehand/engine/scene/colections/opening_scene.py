from thehand.engine.scene import Scene

import pygame


class OpeningScene(Scene):
    def __init__(self, name: str):
        super().__init__(name)

        self.font = pygame.font.Font(None, 36)

    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.flip()
