from thehand.core.scene.scene import Scene
from thehand.core.state import State


class SceneManager:
    def __init__(self, state: State) -> None:
        self._state = state

        self.scenes: dict[str, Scene] = {}

        self._current_scene: Scene | None = None

    def __call__(self) -> None:
        self._current_scene.handle_events()
        self._current_scene.update()
        self._current_scene.render()

    def __add__(self, scene: Scene) -> "SceneManager":
        self.add(scene)
        return self

    def __lshift__(self, scene: Scene) -> None:
        self.set_current(scene.name)

    def set_current(self, scene: str) -> None:
        if not self.scenes.get(scene):
            raise NameError(f'Scene "{scene}" not found!')

        self._current_scene: Scene = self.scenes[scene]
        if not self._current_scene.have_setup:
            self._current_scene.setup()

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def next(self) -> None:
        if not self._current_scene or not self._current_scene.next_scene:
            return

        self.set_current(self._current_scene.next_scene.name)

    def stop(self):
        self._running = False
