from collections import defaultdict
import asyncio


class MiddleWareBase:
    _listeners = defaultdict(list)
    def on(self, event, callback):
        self.add_listener(event, callback, event)

    def trigger(self, event):
        raise NotImplementedError("On should be implemented in a subclass")

    def add_listener(self, event, callback, callback_argument):
        self._listeners[event].append((asyncio.coroutine(callback),
                                        callback_argument))
