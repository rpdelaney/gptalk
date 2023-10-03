class GPTValueError(ValueError):
    """gptalk-specific ValueError."""


class GPTNullInputError(GPTValueError):
    """The ValueError for when the user didn't enter anything."""
