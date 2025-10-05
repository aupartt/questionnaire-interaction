from enum import Enum


class StatusEnum(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class QuestionType(str, Enum):
    TEXT = "text"
    IMG = "image"
    VIDEO = "video"


class ResponseType(str, Enum):
    TEXT = "text"
    LIKERT5 = "likert_5"
