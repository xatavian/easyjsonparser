from .helper import EASY_NONEHELPER
from typing import Any


class EasyJSONValue(object):
    __computed_schema = False
    __schema = None

    def get_schema(self):
        if self.__class__.__computed_schema:
            return self.__class__.__schema

        result = self._get_schema()
        self.__class__.__schema = result
        self.__class__.__computed_schema = True
        return result

    def _get_schema(self):
        return self

    def __init__(self, optional: bool=False, default: Any=EASY_NONEHELPER):
        self._optional = optional
        self._default = default

    def validate(self, srcval):
        raise NotImplementedError()

    def compute(self, srcval):
        return srcval if srcval is not None else self._default

    @property
    def optional(self):
        return self._optional

    @property
    def default(self):
        return self._default
