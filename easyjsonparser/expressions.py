from .object import EasyJSONValue
from .helper import EASY_NONEHELPER

class EasyJSONIntegerValue(EasyJSONValue):
    def validate(self, srcval):
        return isinstance(srcval, int), 'Integer expected'


class EasyJSONBooleanValue(EasyJSONValue):
    def validate(self, srcval):
        return isinstance(srcval, bool), 'Boolean expected'


class EasyJSONStringValue(EasyJSONValue):
    def validate(self, srcval):
        return isinstance(srcval, str), 'String expected'


class EasyJSONFloatValue(EasyJSONValue):
    def validate(self, srcval):
        return isinstance(srcval, float), 'Float expected'


class EasyJSONNullValue(EasyJSONValue):
    def __init__(self, *args, **kwargs):
        if "default" not in kwargs or \
                kwargs["default"] is EASY_NONEHELPER:
            kwargs["default"] = None
        super().__init__(*args, **kwargs)

    def validate(self, srcval):
        return srcval is None, 'Null expected'
