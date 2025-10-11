from engine.scene.scene import Scene


class SceneManager:
    """
    Manage scenes.
    Run only one scene at a time.
    Do scene operations: add, remove, reload, next, previous and handle transition.
    """

    def __init__(self):
        self.scenes: list[Scene]
        self.current_scene: Scene

    def run(self):
        self.current_scene.handle_event()
        self.current_scene.update()
        self.current_scene.render()
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def reload(self):
        pass

    def next(self):
        pass

    def prev(self):
        pass
