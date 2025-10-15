from thehand.core.entity.entity_manager import EntityManager
from thehand.core.scene.scene_state import SceneState


class Updater:
    def __init__(self, state: SceneState, entity: EntityManager):
        self.state = state
        self.entity = entity
        pass

    def __call__(self):
        pass
