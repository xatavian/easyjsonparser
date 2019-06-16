from .value import _Value, _ValueInstance, _raise_bad_value_error
from .helper import Empty


class Null(_Value):
    def compute_instance_type(self):
        result_type = type("NullInstance",
                           (_NullInstance, ),
                           self._default_value_instance_params())
        return result_type

    def check_params(self):
        if self.default is not None:
            _raise_bad_value_error(self.default, "Default value of a Null value can only be None.")
        super().check_params()


class _NullInstance(_ValueInstance):
    def compute_to_json(self):
        return "null"

    def check_and_sanitize_input(self, value):
        if value is None:
            return value
        elif type(self) is type(value):
            return value.value
        elif value is not Empty:
            _raise_bad_value_error(value, self.__property_name__, "None expected")
        else:
            return super().check_and_sanitize_input(value)
