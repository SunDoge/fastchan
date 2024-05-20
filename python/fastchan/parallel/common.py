from dataclasses import dataclass
from fastchan._lowlevel import Receiver, Sender
from typing import Callable, Any


class Worker:
    task_receiver: Receiver
    output_sender: Sender
    func: Callable[[Any], Any]

    def __call__(self):
        pass
