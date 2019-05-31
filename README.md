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

# Usage

TODO

