from thehand.core.audition import Audition
from thehand.core.state import State
from thehand.examples.audition.hello_text_processor import HelloTextProcessor


class HelloAudition(Audition):
    def sr_result_callback(self, text: str) -> None:
        result = self.hello_text_processor(text)
        if result:
            print("(*/ω＼*)")
        return None

    def __init__(self, state: State | None = None) -> None:
        super().__init__(state)

        self.hello_text_processor: HelloTextProcessor = HelloTextProcessor()
