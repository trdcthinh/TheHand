from thehand.examples.audition.hello_text_processor import HelloTextProcessor
from thehand.core.audition import BaseAudition
from thehand.core.state import StateManager


class HelloAudition(BaseAudition):
    def sr_result_callback(self, text: str) -> None:
        result = self.hello_text_processor(text)
        if result:
            print("(*/ω＼*)")
        return None

    def __init__(self, state: StateManager | None = None) -> None:
        super().__init__(state)

        self.hello_text_processor: HelloTextProcessor = HelloTextProcessor()
