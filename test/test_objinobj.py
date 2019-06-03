from easyjsonparser.document import JSONObjectDocument
import easyjsonparser as ejp


class TestObjectWithObject(JSONObjectDocument):
    class ObjectProperty(ejp.Object):
        attr1 = ejp.String()
        attr2 = ejp.Integer()
    prop = ObjectProperty()

obj1 = TestObjectWithObject.load({
    "prop": {
        "attr1": "1", "attr2": 1
    }
})
obj2 = TestObjectWithObject.load({
    "prop": {
        "attr1": "2", "attr2": 2
    }
})

print(obj1.to_json())
print(obj2.to_json())