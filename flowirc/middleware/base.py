from collections import defaultdict
import asyncio
from flowirc.log import log


class MiddleWareBase:
    _listeners = defaultdict(list)

    def on(self, event, callback):
        self.add_listener(event, callback, event)

    @asyncio.coroutine
    def trigger(self, event):
        log.debug("Received event: %s", event)
        listeners = self._listeners[event]

        for future in asyncio.as_completed(
                [callback(evant) for callback, event_type in
                 listeners if self.matches(event, event_type)]):
            result = yield from future
            self.dispatch(result)

    def add_listener(self, event, callback, callback_argument):
        self._listeners[event].append((asyncio.coroutine(callback),
                                       callback_argument))

    def dispatch(self, data):
        raise NotImplementedError()
