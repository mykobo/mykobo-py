release:
	semantic-release version --changelog

test:
	@source .venv/bin/activate && poetry run pytest

# Regenerate the notification_contract canonical snapshot from registry.yaml.
update-registry-snapshot:
	@source .venv/bin/activate && poetry run python scripts/regenerate_snapshot.py

# Cross-library snapshot equivalence check. PEER defaults to ../mykobo-rs.
PEER ?= ../mykobo-rs
verify-peer:
	@diff -u \
		tests/fixtures/notification_contract/registry.canonical.json \
		$(PEER)/tests/fixtures/notification_contract/registry.canonical.json \
		&& echo "registry snapshots match peer at $(PEER)"