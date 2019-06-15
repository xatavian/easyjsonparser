from .value import _Value, _ValueInstance, _raise_bad_value_error
from .helper import Empty


class String(_Value):
    """
    Schema-class for JSON strings.
    """

    def compute_instance_type(self):
        result_type = type("StringInstance",
                           (_StringInstance, ),
                           self._default_value_instance_params())
        return result_type

    def check_params(self):
        if isinstance(self.default, str):
            return
        super().check_params()


class _StringInstance(_ValueInstance):
    def __repr__(self):
        return "<JSON Value {classname}: {value}>".format(
            classname=self.__class__.__name__,
            value='"{}"'.format(self.value)
                  if isinstance(self.value, str) else self.value
        )

    def compute_to_json(self):
        return '"{}"'.format(self.value)

    def check_and_sanitize_input(self, value):
        if isinstance(value, str):
            return value
        elif value is not Empty():
            _raise_bad_value_error(
                value, self.__property_name__, "String type expected")
        else:
            return super().check_and_sanitize_input(value)
