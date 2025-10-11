from enums import ProcessStatus, Command


class TextProcessor:
    def __init__(self):
        self._target_sentences: list[str] = []
        pass

    def __call__(self) -> Command:
        return Command.DO_SOMETHING
        pass

    def set_targets(self, targets: list[str]):
        self._target_sentences = targets

    def get_status(self) -> ProcessStatus:
        return ProcessStatus.WAITING
        pass

    def get_accuracy(self) -> float:
        return 0
        pass
