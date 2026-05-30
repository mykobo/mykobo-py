from mykobo_py.message_bus.models.base import EventType


NOTIFICATION_EVENTS: frozenset[EventType] = frozenset({
    EventType.RELAY_INITIATED,
    EventType.RELAY_COMPLETED,
    EventType.RELAY_ONBOARDED,
    EventType.RELAY_STUCK_DEPOSITING,
    EventType.RELAY_STUCK_BRIDGING,
    EventType.RELAY_STUCK_FORWARDING,
    EventType.RELAY_FORWARDING_FAILED,
    EventType.CIRCLE_API_5XX_BURST,
    EventType.WEBHOOK_REPROCESSOR_BACKLOG,
})
