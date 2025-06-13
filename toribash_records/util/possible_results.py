from enum import Enum


class MatchResult(Enum):
    DECISION = ["via decision.", "via unanimous decision.", "via split decision.", "via majority decision."]
    FORFEIT = ["via forfeit."]
    TKO = ["via tko."]
    DRAW = ["unanimous draw.", "split draw.", "majority draw.", "draw."]
    SUBMISSION = ["via submission."]
    UNDOCUMENTED = ["undocumented."]

    @classmethod
    def from_text(cls, text:str):
        for member in cls:
            if text.lower() in member.value:
                return member
        return None
