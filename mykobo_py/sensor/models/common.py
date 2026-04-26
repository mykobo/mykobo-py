from enum import Enum


class Chain(str, Enum):
    STELLAR = "STELLAR"
    SOLANA = "SOLANA"
    BASE = "BASE"


class EnrichmentStrategy(str, Enum):
    MEMO = "MEMO"
    INTENT_MATCH = "INTENT_MATCH"


class TransactionStatus(str, Enum):
    RECEIVED = "RECEIVED"
    DISPATCHED = "DISPATCHED"
    UNMATCHED = "UNMATCHED"
    FAILED = "FAILED"
