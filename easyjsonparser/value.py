from .helper import Empty
from typing import Any
from .instance import InstanceCreator


def _raise_conversion_warning():
    print("Warning: conversion will happen")


def _raise_bad_value_error(value, property_name=None, explanation=""):
    if property_name is None:
        raise RuntimeError("Error: invalid value {value}. {explanation}".format(value=value, explanation=explanation))
    raise RuntimeError("Error: invalid value {value} for property {property}. "
                       "{explaination}".format(value=value,
                                               property=property_name,
                                               explaination=explanation))


class _Value(object):
    """
    <Abstract class>
    Represents any JSON value.
    Constructor arguments:
    -> default: During parsing, value to provide if none is supplied
    """
    __property_name__ = None
    # @classmethod
    # def get_schema(cls):
    #     if cls.__schema is not EASY_NONEHELPER:
    #         return cls.__schema
    #
    #     result = cls.compute_schema()
    #     cls.__schema = result
    #     return result
    #
    # @classmethod
    # def compute_schema(cls):
    #     return cls

    def compute_instance_type(self):
        return type("ValueType",
                    (_ValueInstance,),
                    self._default_value_instance_params())

    def _default_value_instance_params(self):
        return {
            "__default__": self.default,
            "__optional__": self.is_optional,
            "__property_name__": self.__property_name__
        }

    def __init__(self, default: Any=Empty, optional: bool=False):
        self._default = default
        self._optional = optional
        self._instance_creator = InstanceCreator()

        self.check_params()
        self._instance_creator.compute_instance_type(self.compute_instance_type)

    def check_params(self):
        if self.default is not Empty:
            raise RuntimeError('BadValueError: Unexpected class type '
                               '"{value_type}" for the default value'.format(value_type=type(self.default)))

    @property
    def is_optional(self):
        return self._optional

    @property
    def default(self):
        return self._default

    def __call__(self, *args, **kwargs):
        return self._instance_creator.instance_type(*args, **kwargs)


class _ValueInstance(object):
    __default__ = Empty
    __optional__ = False
    __explanations__ = {
        "missing_value": "You must set a value to the parameter in order to print it"
    }
    __property_name__ = None

    def __init__(self, value: Any=Empty):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, next_value):
        self._value = self.check_and_sanitize_input(next_value)

    def __repr__(self):
        return '<JSON Value {classname}: {value}>'.format(
            classname=self.__class__.__name__,
            value=self.value
        )

    def __str__(self):
        return self.__repr__()

    @property
    def is_optional(self):
        return self.__optional__

    def check_and_sanitize_input(self, value):
        if value is not Empty:
            raise RuntimeError("Error: trying to unset a value while it is not optional")
        return value

    def fill(self, src):
        # print("Fill", self.__class__.__name__)
        self.value = src

    def to_json(self):
        if self.value is Empty and not self.is_optional:
            _raise_bad_value_error(self.value, self.__property_name__, _ValueInstance.__explanations__["missing_value"])
        return self.compute_to_json()

    def compute_to_json(self):
        raise NotImplementedError()
