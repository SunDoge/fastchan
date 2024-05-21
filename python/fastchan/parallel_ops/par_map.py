import fastchan
from dataclasses import dataclass
from typing import Iterable, Callable


def producer(source, tx):
    def f():
        for x in source:
            tx.send(x)

    return f


def consumer(func, rx, tx):
    def f():
        for x in fastchan.iter_receiver(rx):
            tx.send(func(x))

    return f


def flat_consumer(func, rx, tx):
    def f():
        for x in fastchan.iter_receiver(rx):
            for y in func(x):
                tx.send(y)

    return f


@dataclass
class ParMap:
    source: Iterable
    func: Callable
    num_threads: int = 1
    in_capacity: int = 100
    out_capacity: int = 100

    def __iter__(self):
        if self.num_threads == 0:
            for x in self.source:
                yield self.func(x)
        else:
            tx1, rx1 = fastchan.bounded(self.in_capacity)
            tx2, rx2 = fastchan.bounded(self.out_capacity)

            fastchan.spawn(producer(self.source, tx1))
            del tx1

            for _thread_idx in range(self.num_threads):
                fastchan.spawn(consumer(self.func, rx1, tx2))
            del tx2

            yield from fastchan.iter_receiver(rx2)


@dataclass
class ParFlatMap:
    source: Iterable
    func: Callable
    num_threads: int = 1
    in_capacity: int = 100
    out_capacity: int = 100

    def __iter__(self):
        if self.num_threads == 0:
            for source in self.source:
                for x in source:
                    yield self.func(x)
        else:
            tx1, rx1 = fastchan.bounded(self.in_capacity)
            tx2, rx2 = fastchan.bounded(self.out_capacity)

            fastchan.spawn(producer(self.source, tx1))
            del tx1

            for _thread_idx in range(self.num_threads):
                fastchan.spawn(flat_consumer(self.func, rx1, tx2))
            del tx2

            yield from fastchan.iter_receiver(rx2)
