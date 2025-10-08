from enum import Enum

from pydantic import BaseModel


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


class ResultStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class Result(BaseModel):
    status: ResultStatus
    message: str


class VerifyResult(BaseModel):
    is_valid: bool
