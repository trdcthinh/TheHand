import pygame as pg

from thehand.core.event import Event, EventCode, create_next_scene_event
from thehand.core.scene.scene import Scene
from thehand.core.state import State


class SceneManager:
    def __init__(self, state: State) -> None:
        self.state = state

        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None

        self.clock = pg.time.Clock()

        self._running = False

    def run(self):
        if len(self.scenes) == 0:
            raise IndexError("No scene!")

        if not self.current_scene:
            raise AttributeError("No current scene")

        self._running = True
        while self._running:
            events = self._handle_events()

            if not self.current_scene:
                print("No scene!")
                self.clock.tick(5)
                continue

            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.render()

            self.clock.tick(self.state.FPS)

    def stop(self):
        self._running = False

    def _handle_events(self) -> list[pg.event.Event]:
        events = pg.event.get()

        for event in events:
            if event.type == Event.COMMAND.value:
                if event.code == EventCode.COMMAND_NEXT_SCENE:
                    self.next()

        return events

    def set_current(self, scene: str) -> None:
        if not self.scenes.get(scene):
            raise NameError(f'Scene "{scene}" not found!')

        self.current_scene: Scene = self.scenes[scene]
        if not self.current_scene.have_setup:
            self.current_scene.setup()

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def next(self) -> None:
        if not self.current_scene or not self.current_scene.next_scene:
            pg.event.post(create_next_scene_event())
            return

        self.set_current(self.current_scene.next_scene.name)

    def __add__(self, scene: Scene) -> "SceneManager":
        self.add(scene)
        return self

    def __lshift__(self, scene: Scene) -> None:
        self.set_current(scene.name)
