import pygame

from thehand.engine.entity.entity_manager import EntityManager
from thehand.engine.scene.renderer import Renderer
from thehand.engine.scene.scene_state import SceneState
from thehand.engine.scene.updater import Updater


class Scene:
    """
    Building block of the game.
    A game can have many Scene managed by SceneManager.
    Each hold its unique SceneState, EntityManager but not necessarily Updater and Renderer.
    """

    def __init__(self, name: str, screen: pygame.Surface):
        self.name = name
        self.screen = screen

        self.state = SceneState()
        self.entity = EntityManager()

        self.updater = Updater(self.state, self.entity)
        self.renderer = Renderer(self.state, self.entity)
        pass

    def setup(self):
        pass

    def handle_events(self) -> None:
        pass

    def update(self):
        self.updater()
        pass

    def render(self):
        self.renderer()
        pass

    def cleanup(self):
        pass
