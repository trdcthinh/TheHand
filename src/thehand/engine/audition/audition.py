import time
from threading import Thread

from thehand.engine.audition.speech_recognition import SpeechRecognition
from thehand.engine.audition.text_processor import TextProcessor
from thehand.engine.state import StateManager
from thehand.engine.enums import Command


class Audition:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

        self.sr = SpeechRecognition(callback=self.callback)
        self.processor = TextProcessor()

        self.commands: list[Command] = []

    def __call__(self):
        sr_thread = Thread(target=self.run_speech_recognition, daemon=True)
        sr_thread.start()

        self.run()

    def run(self):
        # TODO
        while True:
            time.sleep(0.2)

    def callback(self, text: str):
        command = self.processor(text)

        if command != Command.DO_NOTHING:
            self.commands.append(command)
            print(f"Added {command}")

    def run_speech_recognition(self):
        self.sr.run()
