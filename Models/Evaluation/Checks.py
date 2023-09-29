from Logic.Structure.Session import Session
from Objects.Internal.Preference.Preference import Rule


class RuleCheck:
    def __init__(self, rule: Rule, session: Session) -> None:
        self.rule = rule
        self.session = session