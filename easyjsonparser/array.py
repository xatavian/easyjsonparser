from .value import EasyJSONValue


class EasyJSONArray(EasyJSONValue):
    def __init__(self, schema, minsize=0, maxsize=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(schema, EasyJSONValue):
            raise RuntimeError("Invalid schema supplied for EasyJSONArray")

        self._schema = schema
        self._minsize = minsize
        self._maxsize = maxsize

    def validate(self, srcval):
        if not isinstance(srcval, list):
            return False, 'Not an array'
        elif len(srcval) < self._minsize:
            return False, 'Array too small'
        elif self._maxsize is not None and len(srcval) > self._maxsize:
            return False, 'Array too large'

        for entry in srcval:
            success, error = self._schema.validate(entry)
            if not success:
                return False, f'Error during schema validation: {error}'
        return True, None

    def compute(self, srcval):
        if srcval is None:
            return self._default

        result = []
        for entry in srcval:
            result.append(self._schema.compute(entry))
        return result
