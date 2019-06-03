from .value import _Value, _ValueInstance, _raise_conversion_warning, _raise_bad_value_error
from .helper import Empty


def _is_convertible(srctype):
    return srctype in (bool, int, float)


class Integer(_Value):
    def compute_instance_type(self):
        result_type = type("IntegerInstance",
                           (_IntegerInstance, ),
                           self._default_value_instance_params())
        return result_type

    def check_params(self):
        if isinstance(self.default, int):
            return
        elif _is_convertible(self.default.__class__):
            _raise_conversion_warning()
            self._default = int(self._default)
        else:
            return super().check_params()


class _IntegerInstance(_ValueInstance):
    def compute_to_json(self):
        return self.value

    def check_and_sanitize_input(self, value):
        if isinstance(value, int):
            return value
        elif _is_convertible(value.__class__):
            _raise_conversion_warning()
            return int(value)
        elif value is not Empty:
            _raise_bad_value_error(value, "Integer type expected")
        else:
            super().check_and_sanitize_input(value)


class Float(_Value):
    def compute_instance_type(self):
        result_type = type("FloatInstance",
                           (_FloatInstance, ),
                           self._default_value_instance_params())
        return result_type

    def check_params(self):
        if not isinstance(self.default, float):
            return
        elif _is_convertible(self.default.__class__):
            _raise_conversion_warning()
            self._default = float(self._default)
        else:
            super().check_params()


class _FloatInstance(_ValueInstance):
    def compute_to_json(self):
        return self.value

    def check_and_sanitize_input(self, value):
        if isinstance(value, float):
            return value
        elif _is_convertible(value.__class__):
            _raise_conversion_warning()
            return float(value)
        elif value is not Empty:
            _raise_bad_value_error(value, self.__property_name__, "Integer type expected")
        else:
            super().check_and_sanitize_input(value)


class Boolean(_Value):
    def compute_instance_type(self):
        result_type = type("BoolInstance",
                           (_BoolInstance, ),
                           self._default_value_instance_params())
        return result_type

    def check_params(self):
        if not isinstance(self.default, bool):
            return
        elif _is_convertible(self.default.__class__):
            _raise_conversion_warning()
            self._default = bool(self._default)
        else:
            super().check_params()


class _BoolInstance(_ValueInstance):
    def compute_to_json(self):
        return self.value

    def check_and_sanitize_input(self, value):
        if isinstance(value, bool):
            return value
        elif _is_convertible(value.__class__):
            _raise_conversion_warning()
            return bool(value)
        elif value is not Empty:
            _raise_bad_value_error(value, self.__property_name__, "Integer type expected")
        else:
            return super().check_and_sanitize_input(value)