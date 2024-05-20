from dataclasses import dataclass
from fastchan._lowlevel import Receiver, Sender
from typing import Callable, Any


@dataclass
class Worker:
    task_receiver: Receiver
    output_sender: Sender
    func: Callable[[Any], Any]

    def __call__(self):
        for task in self.task_receiver:
            output = self.func(task)
            self.output_sender.send(output)

        del self.output_sender


@dataclass
class Producer:
    pass


@dataclass
class Collector:
    pass
