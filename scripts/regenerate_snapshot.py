"""Regenerate tests/fixtures/notification_contract/registry.canonical.json.

Run: poetry run python scripts/regenerate_snapshot.py
Commit the regenerated file alongside any registry.yaml change.
"""
from pathlib import Path

from mykobo_py.notification_contract import REGISTRY
from mykobo_py.notification_contract.canonical import to_canonical_json

OUT = Path(__file__).parent.parent / "tests" / "fixtures" / "notification_contract" / "registry.canonical.json"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(to_canonical_json(REGISTRY), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
