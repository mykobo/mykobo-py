# Sensor Module Tests — Design

## Goal
Add unit tests for `mykobo_py/sensor/` covering the HTTP client and pydantic response model deserialization.

## Scope
- `tests/sensor/__init__.py`
- `tests/sensor/test_sensor_client.py` — HTTP client behavior using `requests_mock`
- `tests/sensor/test_sensor_models.py` — pydantic model round-trips for `WatchedAddress`, `ChainTransaction`, `Intent`

## Test inventory

### `test_sensor_client.py`
Mirrors the style of `tests/anchor/test_dapp_client.py`. Each test uses the `requests_mock` pytest fixture.

1. `test_client_initialization` — host/logger assigned, API_PREFIX is `/api/v1`.
2. `test_health` — GET `/health` returns 200.
3. `test_list_watched_addresses_no_filters` — GET `/api/v1/watched-addresses`, no query string.
4. `test_list_watched_addresses_with_filters` — `chain` and `enabled=True` become `?chain=STELLAR&enabled=true`.
5. `test_get_watched_address` — GET `/api/v1/watched-addresses/{id}`.
6. `test_create_watched_address` — POST with JSON body that excludes `None` fields; verify body content.
7. `test_update_watched_address` — PATCH with JSON body that excludes `None` fields.
8. `test_delete_watched_address` — DELETE returns 204.
9. `test_list_chain_transactions_with_filters` — verify all four filters (`chain`, `status`, `recipient`, `limit`) appear in query string.
10. `test_get_chain_transaction` — GET by id.
11. `test_list_intents_with_filters` — verify `chain`, `matched=false`, `limit` in query string.
12. `test_get_intent` — GET by id.
13. `test_raises_for_status_on_error` — 500 response causes `HTTPError`.
14. `test_authorization_header_when_token_provided` — supplying a `Token` adds `Authorization: Bearer …`.

### `test_sensor_models.py`
Realistic JSON payloads round-tripped through `model_validate`.

1. `test_watched_address_from_json` — full payload, all fields populated; verify UUID, datetime, list typing, enum coercion.
2. `test_chain_transaction_minimal` — required-only payload; optional fields default to `None`.
3. `test_chain_transaction_full` — full payload including `block_number`, `memo`, `failure_reason`, `raw_data`, `dispatched_at`; verify `Decimal` precision preserved on `amount`.
4. `test_intent_unmatched` — `matched=false`, `chain_transaction_id` is `None`.
5. `test_intent_matched` — `matched=true`, `chain_transaction_id` set.
6. `test_chain_enum_values` — Chain accepts `STELLAR`, `SOLANA`, `BASE`.
7. `test_transaction_status_enum_values` — accepts `RECEIVED`, `DISPATCHED`, `FAILED`.

## Notes
- No new fixtures or stub files; payloads are inline dicts (consistent with existing tests).
- No tests for request models beyond their use in `test_create_watched_address` / `test_update_watched_address` — pydantic-level validation is library behavior, not ours.
