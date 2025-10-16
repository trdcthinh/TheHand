import pygame

from thehand.core.event import Event, EventCode
from thehand.core.scene.scene import Scene
from thehand.core.state import State


class SceneManager:
    def __init__(self, state: State | None = None) -> None:
        self.state: State = state if isinstance(state, State) else State()

        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

    def __call__(self):
        if len(self.scenes) == 0:
            raise IndexError("No scene!")

        if not self.current_scene:
            raise AttributeError("No current scene")

        while True:
            if not self.current_scene:
                print("No scene!")
                self.clock.tick(5)
                continue

            self._handle_events()
            self._update()
            self._render()

            self.clock.tick(self.state.FPS)

    def _handle_events(self) -> None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == Event.COMMAND.value:
                if event.code == EventCode.COMMAND_NEXT_SCENE:
                    self.next()

        self.current_scene.handle_events(events)

    def _update(self) -> None:
        self.current_scene.update()

    def _render(self) -> None:
        self.current_scene.render()

    def run(self, scene: str) -> None:
        if not self.scenes.get(scene):
            raise NameError(f'Scene "{scene}" not found!')
        self.current_scene: Scene = self.scenes[scene]

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def next(self) -> None:
        if not self.current_scene or not self.current_scene.next_scene:
            print("End game!")
            pygame.quit()
            exit(0)

        self.current_scene = self.current_scene.next_scene
