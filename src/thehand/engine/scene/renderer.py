from thehand.engine.entity.entity_manager import EntityManager
from thehand.engine.scene.scene_state import SceneState


class Renderer:
    def __init__(self, state: SceneState, entity: EntityManager):
        self.state = state
        self.entity = entity
        pass

    def __call__(self):
        pass
