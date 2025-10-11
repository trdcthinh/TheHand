from engine.entity.entity_manager import EntityManager
from engine.scene.scene_state import SceneState
from engine.scene.renderer import Renderer
from engine.scene.updater import Updater


class Scene:
    """
    Building block of the game.
    A game can have many Scene managed by SceneManager.
    Each hold its unique SceneState, EntityManager but not necessarily Updater and Renderer.
    """

    def __init__(self, name: str):
        self.name = name

        self.state = SceneState()
        self.entity = EntityManager()

        self.updater = Updater(self.state, self.entity)
        self.renderer = Renderer(self.state, self.entity)
        pass

    def setup(self):
        pass

    def handle_event(self):
        pass

    def update(self):
        self.updater()
        pass

    def render(self):
        self.renderer()
        pass

    def cleanup(self):
        pass
