from audition.speech_recognition import SpeechRecognition
from audition.text_processor import TextProcessor


class Audition:
    def __init__(self):
        self.sr = SpeechRecognition()
        self.processor = TextProcessor()

    def __call__(self):
        pass
