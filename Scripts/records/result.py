from enum import Enum


class MatchResult(Enum):
    DECISION = "via decision."
    SPLIT_DECISION = "via split decision."
    MAJORITY_DECISION = "via majority decision."
    UNANIMOUS_DECISION = "via unanimous decision."
    DRAW = "draw."
    SPLIT_DRAW = "split draw."
    MAJORITY_DRAW = "majority draw."
    UNANIMOUS_DRAW = "unanimous draw."
    SUBMISSION = "via submission."
    KNOCKOUT = "via tko."
    FORFEIT = "via forfeit."
    UNDOCUMENTED = "undocumented."