from enum import Enum


class StatusEnum(Enum):
    IN_PROGRESS = "in_progress"
    ENDED = "ended"


class QuestionType(Enum):
    TEXT = "text"


class ResponseType(Enum):
    TEXT = "text"
    LIKERT5 = "likert_5"
