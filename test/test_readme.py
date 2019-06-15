from easyjsonparser.document import JSONObjectDocument, \
                                    JSONArrayDocument
import easyjsonparser as ejp
import unittest


class User(JSONObjectDocument):
    id = ejp.String()
    username = ejp.String()
    age = ejp.Integer()
    isAdmin = ejp.Boolean()


class UserList(JSONArrayDocument):
    schema = User()


class ReadmeTestCase(unittest.TestCase):
    def test_user_load(self):
        user = User.load({
            "id": "xxx047AD_",
            "username": "jsonisnice",
            "age": 16,
            "isAdmin": False
        })
        self.assertEqual(user.id, "xxx047AD_")
        self.assertEqual(user.username, "jsonisnice")
        self.assertEqual(user.age, 16)
        self.assertEqual(user.isAdmin, False)

    def test_users_load(self):
        users = UserList.load([
            {"id": "1", "username": "test",
             "age": 13, "isAdmin": False},
            {"id": "2", "username": "test2",
             "age": 14, "isAdmin": False}
        ])
        self.assertEqual(len(users), 2)
