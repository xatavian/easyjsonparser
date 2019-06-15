from .helper import Empty
from typing import Any
from .instance import InstanceCreator


def _raise_conversion_warning():
    print("Warning: conversion will happen")


def _raise_bad_value_error(value, property_name=None, explanation=""):
    if property_name is None:
        raise RuntimeError("Error: invalid value {value}. {explanation}"
                           .format(value=value, explanation=explanation))
    raise RuntimeError("Error: invalid value {value} for property {property}. "
                       "{explaination}".format(value=value,
                                               property=property_name,
                                               explaination=explanation))


class _Value(object):
    """
    <Abstract class>
    Represents any JSON schema. When calling the __call__ magic method, it
    creates a new instance of the given schema.

    Schema parameters:
    -> default: During parsing, value to provide if none is supplied
    -> optional: During conversion to a string, indicates if the value can be
                 skipped if no data is provided

    Use _Value.Empty() (or ejp.Empty()) to define empty values
    """
    __property_name__ = None
    Empty = Empty
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
            "__property_name__": self.__property_name__,
            "__schema__": self
        }

    def __init__(self, default: Any = Empty, optional: bool = False):
        self._default = default
        self._optional = optional
        self._instance_creator = InstanceCreator()

        self.check_params()
        self._instance_creator.compute_instance_type(self.compute_instance_type)

    def check_params(self):
        if self.default is not Empty:
            raise RuntimeError('BadValueError: Unexpected class type '
                               '"{value_type}" for the default value'
                               .format(value_type=type(self.default)))

    @property
    def is_optional(self):
        return self._optional

    @property
    def default(self):
        return self._default

    def __call__(self, *args, **kwargs):
        return self._instance_creator.instance_type(*args, **kwargs)


class _ValueInstance(object):
    """
    <Abstract class>
    Base-class for any class that represents a JSON value: string, integer, ...
    but also objects and arrays.
    """
    __default__ = Empty()  # Default value for every instance of a schema
    __optional__ = False  # Indicates if the schema accepts a missing value

    # property-name if the value instance is part of
    # a JSON object
    __property_name__ = None

    # List of predefined string used for common errors
    __explanations__ = {
        "missing_value": "You must set a value to the parameter "
                         "in order to print it"
    }

    def __init__(self, value: Any = Empty()):
        self.value = value

    def __repr__(self):
        return '<JSON Value {classname}: {value}>'.format(
            classname=self.__class__.__name__,
            value=self.value
        )

    def __str__(self):
        return self.__repr__()

    @property
    def value(self):
        """
        The current data of the value instance. When setting a new
        value, a sanitazation check occurs: we make sure that the
        value follows the required schema
        """
        return self.__value

    @value.setter
    def value(self, next_value):
        val = self.check_and_sanitize_input(next_value)
        self.__value = val

    @property
    def is_optional(self):
        """
        Indicates if the field can be omitted during serialization to
        JSON.
        """
        return self.__optional__

    @property
    def default(self):
        """
        The default data of the value instance.
        """
        return self.__default__

    def check_and_sanitize_input(self, value):
        if value is not Empty():
            raise RuntimeError("Error: trying to unset a value "
                               " while it is not optional")
        return value

    def to_json(self):
        """
        Returns the string representation of the value. Raises an
        error if the value is Empty() and not optional.
        """
        if self.value is Empty() and not self.is_optional:
            _raise_bad_value_error(
                self.value,
                self.__property_name__,
                _ValueInstance.__explanations__["missing_value"]
            )
        elif self.value is Empty():
            return ""
        return self.compute_to_json()

    def compute_to_json(self):
        raise NotImplementedError()

    def find(self, targetschema):
        """
        Returns the first instance that matches the given schema or Empty()
        if none was found.
        """
        return Empty()

    def find_all(self, targetschema):
        """
        Returns a list of all the instances that match the given
        schema
        """
        return []
