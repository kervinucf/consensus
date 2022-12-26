from lib.Events.event_controller import subscribe_to_event, post_event
from lib.Twitter.events.listeners import subscribe_to_stream, filtered_stream, unfiltered_stream


def setup_event_handlers():
    subscribe_to_event("new_connection", subscribe_to_stream)
    subscribe_to_event("filtered tweet found", filtered_stream)
    subscribe_to_event("unfiltered tweet found", unfiltered_stream)
