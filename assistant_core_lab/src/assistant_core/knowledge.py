import csv
import json
from dataclasses import dataclass
from pathlib import Path
from assistant_core.errors import DataError

@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str

class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]):
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory":
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            return cls({r["name"].lower(): Office(r["name"], r["room"], r["hours"]) for r in rows})
        except Exception as exc:
            raise DataError(f"office file not found or malformed: {path}") from exc

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)

@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str

class Handbook:
    def __init__(self, rules: list[Rule]):
        self._rules = rules

    @classmethod
    def from_json(cls, path: Path) -> "Handbook":
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
            rules = [Rule(id=item["id"], title=item["title"], text=item["text"]) for item in data]
            return cls(rules)
        except Exception as exc:
            raise DataError(f"handbook file not found or malformed: {path}") from exc

    def search(self, query: str) -> Rule | None:
        words = query.lower().split()
        best_rule = None
        best_score = 0
        for rule in self._rules:
            score = sum(1 for w in words if len(w) > 3 and w in rule.text.lower())
            if score > best_score:
                best_score = score
                best_rule = rule
        return best_rule if best_score >= 1 else None
