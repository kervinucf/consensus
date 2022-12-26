from pymitter import EventEmitter

ee = EventEmitter()


def post_event(event_name: str, event_data=None):
    if event_data is not None:
        ee.emit(event_name, event_data)
    else:
        ee.emit(event_name)


def subscribe_to_event(event_name: str, handler):
    ee.on(event_name, handler)
