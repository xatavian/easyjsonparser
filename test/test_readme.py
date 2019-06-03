from easyjsonparser.document import JSONObjectDocument, JSONArrayDocument
import easyjsonparser as ejp


class User(JSONObjectDocument):
    id = ejp.String()
    username = ejp.String()
    age = ejp.Integer()
    isAdmin = ejp.Boolean()

class UserList(JSONArrayDocument):
    schema = User()

user = User.load({
    "id": "xxx047AD_",
    "username": "jsonisnice",
    "age": 16,
    "isAdmin": False
})

users = UserList.load([
    {"id": "1", "username": "test", "age": 13, "isAdmin": False},
    {"id": "2", "username": "test2", "age": 14, "isAdmin": False}
])
print(user)
print(user.to_json())
print(users)