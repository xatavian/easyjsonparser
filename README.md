EasyJSONParser, a lightweight library for parsing and validating your
JSON models
=================================================================================

Modern Web frameworks all use ORM systems in order to achieve the
server-side actions on the database: for instance, Doctrine for Symfony3
(PHP), Mongoose for MongoDB databases.

ORMs have the ability to read data and convert it into a collections of
in-memory objects. They can also take a special object and convert it
to the underlying storage format.

**Motivation behind this project**

While ORM-like systems are pretty common in Web development, they are
inexistant for all other purposes. For instance, parsing a configuration
file (yeah, that's why I designed this library !) and validating its
content, or outputting the configuration in a file.

# Dependencies

EasyJSONParser only uses the Python's standard library, especially the
[`json`](https://docs.python.org/fr/3/library/json.html) module which
serialize and unserialize the source/target data.

EasyJSONParser is built for Python 3.

# Installation

Get the library from Pypi:

```bash
> pip install easyjsonparser
```

# Basic examples

In this section, we will define dummy data structure `User` which follows the following schema:

```json
{
    "id": "xxx047AD_",
    "username": "jsonisnice",
    "age": 16,
    "isAdmin": false
}
```

`EasyJSONParser` can extract parse the data string into an object with the following code:

```python
import easyjsonparser as ejp
from easyjsonparser.document import JSONObjectDocument

class User(JSONObjectDocument):
    id = ejp.String()
    username = ejp.String()
    age = ejp.Integer()
    isAdmin = ejp.Boolean()

# In this example, the data string is directly
# written in the code but it can have
# various source such as reading a file...
data_string = """
...
"""

user = User.loads(data_string)
```

What if you already have loaded your data into a dictionary ? Then, just use `load` instead of `loads`:

```python
user = User.load({
    "id": "xxx047AD_",
    "username": "jsonisnice",
    "age": 16,
    "isAdmin": False
})
```

We can get a representation of our user instance by just printing it:
```python
>>> print(user)
<JSON UserInstance: {"id": <JSON Value StringInstance: "xxx047AD_">,
 "username": <JSON Value StringInstance: "jsonisnice">, "age": <JSON
  Value IntegerInstance: 16>, "isAdmin": <JSON Value BoolInstance: False>}>
```

What if we now want to parse a list of `User` ?

```python
from easyjsonparser.document import JSONAArrayDocument

class UserList(JSONArrayDocument);
    schema = User()

users = UserList.load([
    { ... },
    { ... }
])
```

Document-type objects (ie. the ones that inherit from either `JSONObjectDocument` or `JSONArrayDocument`) can be mixed into one another.

They also are a variety of types but but the top-level data structure must **always** be either a `JSONObjectDocument` or `JSONArrayDocument`.

Well, now what if we want to turn it back to a JSON string ? Let's use `to_json()` !

```python
>>>  user.to_json()
'{"id": "xxx047AD_", "username": "jsonisnice", "age": 16, "isAdmin": False}'
```
# Documents

Documents are classes that inherits from either `JSONObjectDocument` or `JSONArrayDocument`. They are special kinds of `Object` and `Array` because they contain class methods used for parsing the data. They behave like normal `Object` and `Array` but have the capacity of being a top-level data structure.

The definition of a `JSONArrayDocument` is a little bit different than using a regular `ejp.Array()`: the schema must be defined as a class attribute instead of a constructor argument.

```python
class StringList(JSONArrayDocument):
    schema = String()
```

Here are the following special methods:

**`JSONObjectDocument.load(obj=None)` (@classmethod)**

Creates a `JSONObjectDocument` with input source `obj`. If no input is given, then an empty data structure is computed. If an input is given but is not a dictionnary, an exception is raised.

**`JSONObjectDocument.loads(obj_string)` (@classmethod)**

Creates a `JSONObjectDocument` from a string. The data is parsed to a dictionary using `json.loads()` from Python's standard library. If  `obj_string` does not repressent a valid JSON object, an exception is raised.

**`JSONArrayDocument.load(*values)` (@classmethod)**

Creates a `JSONArrayDocument` from a list of values. `values` can be a variadic array but it is also possible to pass a single input which must be a list or tuple.

**`JSONArrayDocument.loads(array_string)` (@classmethod)**

Creates a `JSONArrayDocument` from a string. The data is parsed to an array using `json.loads()` from Python's standard library. If `array_string` does not represent a valid JSON array, an exception is raised.

# Available types

## `ejp.String()`

Represents a JSON string.

## `ejp.Integer()`

Represents a JSON integer.

*Warning: boolean and floats are accepted as an input but they will be converted to integers with `int()`. A warning is raised when a conversion happens.

*TODO: add an option to disable/enable this behaviour*

## `ejp.Float()`

Represents a floating-point number. Conversion from integers and boolean work the way as `ejp.Integer()`

## `ejp.Boolean()`

Represents a boolean. Conversion from floating-point numbers and boolean work the way as `ejp.Integer()`

## `ejp.Null()`

Represents a `null` value. Every input that is not `None` (in Python) or `null`(as a JSON string) will raise a parsing exception.

## `ejp.Object()`

Represents a JSON object.

Properties cannot be defined in the constructor: they must be defined as class attributes as follows:

```python
class MyObject(ejp.Object):
    property1 = ejp.String()
    property2 = ejp.Boolean()
    ...
```

*Note: remember that you need to use `JSONObjectDocument` to define a top-level object*.

## `ejp.Array()`

Represents a JSON array. An array must follow a schema which must be passed to the constructor of `ejp.Array()`. If the schema is invalid, an exception is raised.

```python
class MyObject(ejp.Object):
    array = ejp.Array(schema=String())
```

*Note: remember that you need to use `JSONArrayDocument` to define a top-level array*.

## `ejp.Empty()`

Represents an empty value. Used for optional properties/values: if you want to clear the content of an optional parameter, set its value to `ejp.Empty()`.

# License

This software is distributed under the [MIT license](LICENSE)