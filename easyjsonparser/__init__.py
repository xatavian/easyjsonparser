from .array import EasyJSONArray
from .object import EasyJSONObject
from .document import EasyJSONDocument
from .expressions import EasyJSONStringValue, EasyJSONIntegerValue, EasyJSONBooleanValue, \
                         EasyJSONFloatValue, EasyJSONNullValue
from .value import EasyJSONValue


class EasyJSONOrValue(EasyJSONValue):
    def __init__(self, schemas=tuple(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(schemas, tuple) or isinstance(schemas, list) \
                or any(not isinstance(s, EasyJSONValue) for s in schemas):
            raise RuntimeError("schemas is expected to be a tuple or list of EasyJSONValue")
        elif len(schemas) == 0:
            raise RuntimeError("EasyJSONOrValue expects at least 1 schema")

        self._schemas = schemas
        self._lastValidatedIndex = -1

    def validate(self, srcval):
        errors = []
        for i, s in enumerate(self._schemas):
            success, error = s.validate(srcval)
            if success:
                self._lastValidatedIndex = i
                return True, None
            errors.append(error)

        self._lastValidatedIndex = -1
        return False, '/'.join(errors)

    def compute(self, srcval):
        # if self._lastValidatedIndex >= 0:
        #    return self._schemas[self._lastValidatedIndex].compute(srcval)
        for s in self._schemas:
            success, error = s.validate(srcval)
            if success:
                return s.compute(srcval)
        raise RuntimeError("EasyJSONOrValue unexpectidely found no valid schema to "
                           "compute the value")


