from enum import Enum


class MatchResult(Enum):
    DECISION = "via decision."
    CLOSE_DECISION = "10-9"
    MEDIUM_DECISION = "10-8"
    STRONG_DECISION = "10-7"
    GODLY_DECISION = "10-6"
    WTF_DECISION = "10-5"
    SUBMISSION = "via submission."
    KNOCKOUT = "via tko."
    UNDOCUMENTED = "undocumented."

    #TODO figure out a less ass way of doing this bs
    @classmethod
    def from_line(cls, line):
        if line.lower().endswith(cls.DECISION.value):
            return MatchResult.DECISION
        elif line.endswith(cls.CLOSE_DECISION.value):
            return MatchResult.CLOSE_DECISION
        elif line.endswith(cls.MEDIUM_DECISION.value):
            return MatchResult.MEDIUM_DECISION
        elif line.endswith(cls.STRONG_DECISION.value):
            return MatchResult.STRONG_DECISION
        elif line.endswith(cls.GODLY_DECISION.value):
            return MatchResult.GODLY_DECISION
        elif line.endswith(cls.WTF_DECISION.value):
            return MatchResult.WTF_DECISION
        elif line.lower().endswith(cls.SUBMISSION.value):
            return MatchResult.SUBMISSION
        elif line.lower().endswith(cls.KNOCKOUT.value):
            return MatchResult.KNOCKOUT
        elif line.lower().endswith(cls.UNDOCUMENTED.value):
            return MatchResult.UNDOCUMENTED


