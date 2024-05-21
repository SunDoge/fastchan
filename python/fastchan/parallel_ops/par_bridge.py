from dataclasses import dataclass
from typing import Iterable
import fastchan


def worker(tx: fastchan.Sender, source: Iterable):
    def f():
        for x in source:
            tx.send(x)

    return f


@dataclass
class ParBridge:
    source: Iterable
    capacity: int = 100

    def __iter__(self):
        tx, rx = fastchan.bounded(self.capacity)
        fastchan.spawn(worker(tx, self.source))
        del tx
        yield from fastchan.iter_receiver(rx)
