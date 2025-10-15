from thehand.core.audition import BaseTextProcessor


class HelloTextProcessor(BaseTextProcessor):
    def result_callback(self, result: bool) -> None:
        print(f"You just said {result} that contain 'hello'")

    def __call__(self, text: str) -> bool:
        if "hello" in text.lower():
            return True
        return False

    def __init__(self):
        super().__init__()
