from thehand.core.scene.scene import Scene
from thehand.core.state import State


class SceneManager:
    def __init__(self, state: State) -> None:
        self._state = state

        self.scenes: dict[str, Scene] = {}

        self._current_scene: Scene | None = None

    def __call__(self) -> None:
        if self._current_scene.done:
            self.next()
        self._current_scene.handle_events()
        self._current_scene.update()
        self._current_scene.render()

    def __add__(self, scene: Scene) -> "SceneManager":
        self.add(scene)
        return self

    def __lshift__(self, scene: Scene) -> None:
        self.set_current(scene.name)

    def set_current(self, scene: str) -> bool:
        if not self.scenes.get(scene):
            return False

        self._current_scene: Scene = self.scenes[scene]
        if not self._current_scene.have_setup:
            self._current_scene.setup()
        return True

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def next(self) -> bool:
        if not self._current_scene or not self._current_scene.next_scene:
            return False

        return self.set_current(self._current_scene.next_scene.name)
