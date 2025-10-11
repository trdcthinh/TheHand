from enums import ProcessStatus, Command


class TextProcessor:
    def __init__(self):
        self._targets: list[str] = []
        pass

    def __call__(self, text: str) -> Command | None:
        """
        Process the text to produce `Command`.

        Args:
            text (str): Text recognized from SpeechRecognition. Can be empty, can be so long.
                Examples: "but I don't know", "a", "Hmm...", etc.

        Returns:
            Command: A command to do in game.
        """

        return Command.DO_SOMETHING
        pass

    def set_targets(self, targets: list[str]):
        """
        Set new targets and do side effect.

        Args:
            targets (list[str]): A list of words or sentences.
                Examples: ["We are", "the best.", "The Earth is flat."]
        """

        self._targets = targets

    def get_status(self) -> ProcessStatus:
        """
        Return status of process.

        Returns:
            ProcessStatus: An enum present current status of process.
                Example:
                    WAITING if no word have matched.
                    IN_PROGRESS if have matched some words.
                    SUCCEED if have matched all words.
        """

        return ProcessStatus.WAITING
        pass

    def get_accuracy(self) -> float:
        """
        Return current accuracy of speech.

        Returns:
            float: accuracy from 0 to 1.
                Example: 0.5 if the speech mismatch for half of targets.
        """

        return 0
        pass
