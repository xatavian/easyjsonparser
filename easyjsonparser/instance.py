from .helper import Empty
from typing import Type, Any


class InstanceCreator(object):
    def __init__(self):
        self._instance_type = Empty

    @property
    def instance_type(self) -> Type:
        if self._instance_type is not Empty:
            return self._instance_type
        raise RuntimeError("Trying to access an instance type while none was defined²")

    def compute_instance_type(self, callback):
        self._instance_type = callback()