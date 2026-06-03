from mykobo_py.message_bus.models.base import EventType


NOTIFICATION_EVENTS: frozenset[EventType] = frozenset({
    # Relay / circle health
    EventType.RELAY_INITIATED,
    EventType.RELAY_COMPLETED,
    EventType.RELAY_ONBOARDED,
    EventType.RELAY_STUCK_DEPOSITING,
    EventType.RELAY_STUCK_BRIDGING,
    EventType.RELAY_STUCK_FORWARDING,
    EventType.RELAY_FAILED,
    EventType.CIRCLE_API_5XX_BURST,
    EventType.WEBHOOK_REPROCESSOR_BACKLOG,
    # Circle mint/burn
    EventType.MINT_COMPLETED,
    EventType.BURN_COMPLETED,
    EventType.MINT_HELD,
    EventType.BURN_HELD,
    EventType.MINT_HELD_ALERT,
    EventType.BURN_HELD_ALERT,
    EventType.CUSTOMER_NOTIFY_FAILED,
    EventType.MINT_INFO,
    EventType.BURN_INFO,
})
