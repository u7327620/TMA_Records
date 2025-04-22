from enum import Enum


class MatchResult(Enum):
    CLOSE_DECISION = "10-9"
    MEDIUM_DECISION = "10-8"
    STRONG_DECISION = "10-7"
    GODLY_DECISION = "10-6"
    WTF_DECISION = "10-5"
    SUBMISSION = "SUBMISSION"
    KNOCKOUT = "ko"
