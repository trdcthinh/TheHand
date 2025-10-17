import time
from queue import Queue

import numpy as np
from moonshine_onnx import MoonshineOnnxModel, load_tokenizer
from silero_vad import VADIterator, load_silero_vad
from sounddevice import InputStream

from thehand.core.state import State
from thehand.core.types import SrResultCallback

DEFAULT_MODEL = "moonshine/tiny"
SAMPLING_RATE = 16000
CHUNK_SIZE = 512
LOOKBACK_CHUNKS = 5
MAX_SPEECH_SECS = 10
MIN_REFRESH_SECS = 0.2
MAX_LINE_LENGTH = 80


class Transcriber:
    def __init__(self, model_name):
        self.model = MoonshineOnnxModel(model_name=model_name)
        self.rate = SAMPLING_RATE
        self.tokenizer = load_tokenizer()
        self.__call__(np.zeros(self.rate, dtype=np.float32))

    def __call__(self, speech):
        tokens = self.model.generate(speech[np.newaxis, :].astype(np.float32))
        text = self.tokenizer.decode_batch(tokens)[0]
        return text


class SpeechRecognition:
    def __init__(
        self, state: State, result_callback: SrResultCallback | None = None
    ) -> None:
        self.state = state
        self.result_callback = result_callback

        self.model = DEFAULT_MODEL

        print(f"Loading Moonshine model '{self.model}' ...")
        self.transcriber = Transcriber(self.model)
        print("Moonshine model loaded.")
        self.vad_model = load_silero_vad(onnx=True)
        self.vad_iterator = VADIterator(
            model=self.vad_model,
            sampling_rate=SAMPLING_RATE,
            threshold=0.5,
            min_silence_duration_ms=300,
        )
        self.q = Queue()
        self.stream = InputStream(
            samplerate=SAMPLING_RATE,
            channels=1,
            blocksize=CHUNK_SIZE,
            dtype=np.float32,
            callback=lambda data, frames, time_, status: self.q.put(
                (data.copy().flatten(), status)
            ),
        )
        self.captions = []
        self.lookback_size = LOOKBACK_CHUNKS * CHUNK_SIZE
        self.speech = np.empty(0, dtype=np.float32)
        self.recording = False
        self._start_time: float = 0

    def set_result_callback(self, callback: SrResultCallback) -> None:
        self.result_callback = callback

    def get_caption(self):
        return " ".join(self.captions)

    def end_recording(self):
        text = self.transcriber(self.speech)
        if self.result_callback:
            self.result_callback(text)
        self.captions.append(text)
        self.speech *= 0.0

    def soft_reset_vad(self):
        self.vad_iterator.triggered = False
        self.vad_iterator.temp_end = 0
        self.vad_iterator.current_sample = 0

    def run(self):
        print("Speech Recognition ready.")
        self.stream.start()
        self.state.sr_running = True

        while True:
            if not self.state.sr_running:
                time.sleep(0.2)
                continue

            chunk, status = self.q.get()
            if status:
                print(status)
            self.speech = np.concatenate((self.speech, chunk))
            if not self.recording:
                self.speech = self.speech[-self.lookback_size :]
            speech_dict = self.vad_iterator(chunk)
            if speech_dict:
                if "start" in speech_dict and not self.recording:
                    self.recording = True
                    self._start_time = time.time()
                if "end" in speech_dict and self.recording:
                    self.recording = False
                    self.end_recording()
            elif self.recording:
                if (len(self.speech) / SAMPLING_RATE) > MAX_SPEECH_SECS:
                    self.recording = False
                    self.end_recording()
                    self.soft_reset_vad()
                if (time.time() - self._start_time) > MIN_REFRESH_SECS:
                    translation = self.transcriber(self.speech)
                    if self.result_callback:
                        self.result_callback(translation)
                    self._start_time = time.time()

    def stop(self):
        self.stream.close()
        if self.recording:
            while not self.q.empty():
                chunk, _ = self.q.get()
                self.speech = np.concatenate((self.speech, chunk))
            self.end_recording()
