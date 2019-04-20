import queue
from constants import *

class Event:
    def __init__(self, ts, index10, index11, index12, index14):
        self.ts = ts
        self.index10 = index10
        self.index11 = index11
        self.index12 = index12
        self.index14 = index14


class FutureEventList:
    def __init__(self):
        self.q =  queue.Queue()
        self.prevEvent = None

    def push(self, evt):
        # self.lock.acquire()
        # ts = self.current_time + time
        # heapq.heappush(self.pq, (ts, evt))
        # self.lock.release()
        if self.prevEvent is None:
            self.q.put(evt)
            self.prevEvent = evt
        else:
            if self.prevEvent.index10 != evt.index10 or self.prevEvent.index11 != evt.index11 or self.prevEvent.index12 != evt.index12 or self.prevEvent.index14 != evt.index14:
                self.q.put(evt)
                self.prevEvent = evt


    def pop(self):
        return self.q.get()


    def is_empty(self):
        return self.q.empty()
