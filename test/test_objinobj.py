from easyjsonparser.document import JSONObjectDocument
import easyjsonparser as ejp
import unittest


class TestObjectWithObject(JSONObjectDocument):
    class ObjectProperty(ejp.Object):
        attr1 = ejp.String()
        attr2 = ejp.Integer()
    prop = ObjectProperty()


class TestObjInObj(unittest.TestCase):
    def test_load(self):
        obj1 = TestObjectWithObject.load({
            "prop": {
                "attr1": "1", "attr2": 1
            }
        })
        self.assertTrue(obj1.prop.attr2, 1)

    @unittest.skip
    def test_find(self):
        obj = TestObjectWithObject.load({
            "prop": {
                "attr1": "1", "attr2": 1
            }
        })
        self.assertEqual(obj.find(ejp.Integer), 1)
        self.assertEqual(obj.find(ejp.String), "1")
