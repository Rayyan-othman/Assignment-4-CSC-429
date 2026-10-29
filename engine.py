from dataclasses import dataclass
from typing import List, Set, Dict, Any


@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:
    """Apply IF-THEN rules until no new facts can be inferred."""

    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        return all(fact in self.facts for fact in rule.antecedents) and rule.consequent not in self.facts

    def run(self) -> None:
        # Higher priority rules are considered first; original order breaks ties.
        ordered_rules = sorted(self.rules, key=lambda rule: -rule.priority)
        while True:
            rule = next((r for r in ordered_rules if self.can_fire(r)), None)
            if rule is None:
                break
            self.facts.add(rule.consequent)
            self.trace.append({
                "rule": rule.name,
                "antecedents": list(rule.antecedents),
                "consequent": rule.consequent,
                "priority": rule.priority,
            })

    def conclusions(self) -> Dict[str, List[str]]:
        return {
            "recommendations": sorted(f.split(":", 1)[1] for f in self.facts if f.startswith("recommend:")),
            "specs": sorted(f.split(":", 1)[1] for f in self.facts if f.startswith("spec:")),
            "other": sorted(f for f in self.facts if not f.startswith(("recommend:", "spec:"))),
        }
