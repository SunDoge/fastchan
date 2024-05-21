from typing import Callable
import threading
from ._lowlevel import Receiver


def iter_receiver(receiver: Receiver):
    while True:
        try:
            yield receiver.recv()
        except RuntimeError:
            break


def spawn(func: Callable[[], None]) -> threading.Thread:
    thread = threading.Thread(target=func)
    thread.start()
    return thread
