from engine.scene.scene import Scene


class SceneManager:
    def __init__(self):
        self.scenes: list[Scene]
        self.current_scene: Scene

    def run_current_scene(self):
        self.current_scene.handle_event()
        self.current_scene.update()
        self.current_scene.render()
        pass
