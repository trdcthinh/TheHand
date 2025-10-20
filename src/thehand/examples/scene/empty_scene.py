import thehand as th


class EmptyScene(th.Scene):
    def __init__(self, name: str, state: th.State, store: th.Store):
        super().__init__(name, state, store)

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return
