import time
from abc import ABC
from threading import Thread

from thehand.core.audition.speech_recognition import SpeechRecognition
from thehand.core.state import State


class Audition(ABC):
    def __init__(self, state: State) -> None:
        self.state = state
        self.sr = SpeechRecognition(state=self.state)

    def __call__(self) -> None:
        sr_thread = Thread(target=self.sr.run(), daemon=True)
        sr_thread.start()

        time.sleep(99999)
