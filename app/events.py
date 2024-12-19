from dataclasses import dataclass, field
from typing import Any
import uuid

@dataclass
class Event():
    event_name: str
    args: dict[str, Any] = field(default_factory=dict)
    id: str = field(default="")


class EventDispatcherSingleton:
    _instance = None

    @dataclass
    class EventDispatcher:
        listeners: dict[str, Any] = field(default_factory=dict)

        def register_listener(self, listener, key: str):
            self.listeners[key] = listener


        def deregister_listener(self, listener, key: str):
            del self.listeners[key]


        def dispatch(self, event: Event): # TODO: Broadcast event = all listeners | Single event = first listener handles
            if event.id == "":
                event.id = str(uuid.uuid4())
            for key, listener in self.listeners.items():
                handled = listener.on_event(event)
                if handled:
                    print(f"{key}: {event.id} EVENT: {event.event_name}")


    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls.EventDispatcher()
        return cls._instance

GlobalEventDispatcher = EventDispatcherSingleton()
