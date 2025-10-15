import time
from abc import ABC, abstractmethod
from threading import Thread

from thehand.core.audition.speech_recognition import SpeechRecognition
from thehand.core.state import StateManager


class BaseAudition(ABC):
    def __init__(self, state: StateManager | None = None) -> None:
        self.state: StateManager = (
            state if isinstance(state, StateManager) else StateManager()
        )
        self.sr: SpeechRecognition = SpeechRecognition(state=self.state)

    def __call__(self) -> None:
        self.sr.result_callback = self.sr_result_callback
        sr_thread = Thread(target=self._run_sr, daemon=True)
        sr_thread.start()

        while True:
            time.sleep(0.2)

    def _run_sr(self):
        self.sr.run()

    @abstractmethod
    def sr_result_callback(self, text: str) -> None:
        raise NotImplementedError
