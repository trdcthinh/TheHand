import time
from abc import ABC, abstractmethod
from threading import Thread

from thehand.core.audition.speech_recognition import SpeechRecognition
from thehand.core.state import State


class Audition(ABC):
    def __init__(self, state: State | None = None) -> None:
        self.state: State = state if isinstance(state, State) else State()
        self.sr: SpeechRecognition = SpeechRecognition(state=self.state)

    def __call__(self) -> None:
        self.sr.result_callback = self.sr_result_callback

        sr_thread = Thread(target=self.sr.run(), daemon=True)
        sr_thread.start()

        time.sleep(99999)

    @abstractmethod
    def sr_result_callback(self, text: str) -> None:
        raise NotImplementedError
