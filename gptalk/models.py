from dataclasses import dataclass
from enum import Enum


@dataclass
class ModelInfo:
    description: str
    max_tokens: int
    training_data: str
    endpoint: str | None


class Model(Enum):
    GPT4 = ModelInfo(
        description=(
            "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration 2 weeks after it is released."
        ),
        max_tokens=8192,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT4_0613 = ModelInfo(
        description=(
            "Snapshot of gpt-4 from June 13th 2023 with function calling data. Unlike gpt-4, this model will not receive updates, and will be deprecated 3 months after a new version is released."
        ),
        max_tokens=8192,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT4_32K = ModelInfo(
        description=(
            "Same capabilities as the base gpt-4 mode but with 4x the context length. Will be updated with our latest model iteration."
        ),
        max_tokens=32768,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT4_32K_0613 = ModelInfo(
        description=(
            "Snapshot of gpt-4-32 from June 13th 2023. Unlike gpt-4-32k, this model will not receive updates, and will be deprecated 3 months after a new version is released."
        ),
        max_tokens=32768,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT3_5_TURBO = ModelInfo(
        description=(
            "Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration 2 weeks after it is released."
        ),
        max_tokens=4096,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT3_5_TURBO_16K = ModelInfo(
        description=(
            "Same capabilities as the standard gpt-3.5-turbo model but with 4 times the context."
        ),
        max_tokens=16384,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT3_5_TURBO_0613 = ModelInfo(
        description=(
            "Snapshot of gpt-3.5-turbo from June 13th 2023 with function calling data. Unlike gpt-3.5-turbo, this model will not receive updates, and will be deprecated 3 months after a new version is released."
        ),
        max_tokens=4096,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    GPT3_5_TURBO_16K_0613 = ModelInfo(
        description=(
            "Snapshot of gpt-3.5-turbo-16k from June 13th 2023. Unlike gpt-3.5-turbo-16k, this model will not receive updates, and will be deprecated 3 months after a new version is released."
        ),
        max_tokens=16384,
        training_data="Up to Sep 2021",
        endpoint="/v1/chat/completions",
    )
    TEXT_DAVINCI_003 = ModelInfo(
        description=(
            "Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports some additional features such as inserting text."
        ),
        max_tokens=4097,
        training_data="Up to Jun 2021",
        endpoint="/v1/completions",
    )
    TEXT_DAVINCI_002 = ModelInfo(
        description=(
            "Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning"
        ),
        max_tokens=4097,
        training_data="Up to Jun 2021",
        endpoint="/v1/completions",
    )
    CODE_DAVINCI_002 = ModelInfo(
        description=("Optimized for code-completion tasks"),
        max_tokens=8001,
        training_data="Up to Jun 2021",
        endpoint="/v1/completions",
    )
    TEXT_MODERATION_LATEST = ModelInfo(
        description=(
            "Most capable moderation model. Accuracy will be slightly higher than the stable model."
        ),
        endpoint="/v1/moderations",
        max_tokens=None,
        training_data=None,
    )
    TEXT_MODERATION_STABLE = ModelInfo(
        description=(
            "Almost as capable as the latest model, but slightly older."
        ),
        max_tokens=None,
        endpoint="/v1/moderations",
        training_data=None,
    )
