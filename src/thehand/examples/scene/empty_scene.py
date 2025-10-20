from thehand.core import Scene, State, Store


class EmptyScene(Scene):
    def __init__(self, name: str, state: State, store: Store):
        super().__init__(name, state, store)

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return
