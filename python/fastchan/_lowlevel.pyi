from typing import Tuple, Generic, TypeVar

T = TypeVar("T")

class Sender(Generic[T]):
    def send(self, x: T): ...

class Receiver(Generic[T]):
    def recv(self) -> T: ...

def bounded(cap: int) -> Tuple[Sender, Receiver]: ...
