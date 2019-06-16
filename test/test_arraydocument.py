import unittest
from easyjsonparser.document import JSONArrayDocument
from easyjsonparser.array import _ArrayInstance
import easyjsonparser as ejp


class SimpleArray(JSONArrayDocument):
    class SchemaObject(ejp.Object):
        attr1 = ejp.Integer()
        attr2 = ejp.String()
    schema = SchemaObject()


class TestArrayDocument(unittest.TestCase):
    test_string = """[
        {"attr1": 10, "attr2": "string1"},
        {"attr1": 20, "attr2": "string2"}
    ]"""

    def test_loads(self):
        array = SimpleArray.loads(self.test_string)
        self.assertTrue(isinstance(array, _ArrayInstance))
        self.assertEqual(array[0].attr1, 10)
        self.assertEqual(array[1].attr1, 20)

    def test_find(self):
        array = SimpleArray.loads(self.test_string)
        self.assertEqual(array.find(SimpleArray.SchemaObject), array[0])

    def test_to_json(self):
        array = SimpleArray.loads(self.test_string)
        self.assertEqual(array.to_json(),
                         '[{"attr1": 10, "attr2": "string1"}, '
                         '{"attr1": 20, "attr2": "string2"}]')
