from pathlib import Path

from mykobo_py.notification_contract import REGISTRY
from mykobo_py.notification_contract.canonical import to_canonical_json

SNAPSHOT = Path(__file__).parent.parent / "fixtures" / "notification_contract" / "registry.canonical.json"


def test_registry_matches_committed_snapshot():
    expected = SNAPSHOT.read_text(encoding="utf-8")
    actual = to_canonical_json(REGISTRY)
    assert actual == expected, (
        "Registry no longer matches the committed canonical snapshot. "
        "Run `poetry run python scripts/regenerate_snapshot.py` and commit the result."
    )
