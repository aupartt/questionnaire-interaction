from enum import Enum


class StatusEnum(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class QuestionType(Enum):
    TEXT = "text"


class ResponseType(Enum):
    TEXT = "text"
    LIKERT5 = "likert_5"
