from json.decoder import JSONDecodeError


class GPTValueError(ValueError):
    """gptalk-specific ValueError."""


class GPTNullInputError(GPTValueError):
    """The ValueError for when the user didn't enter anything."""


class GPTFileNotFoundError(FileNotFoundError):
    """We couldn't find a file we need."""


class GPTSubsNotFoundError(GPTFileNotFoundError):
    """We couldn't find the subtitles file."""


class GPTJSONDecodeError(JSONDecodeError):
    """We failed to parse JSON."""
