class User:
    def __init__(self, name, email):
        self._name = name
        self._email = email

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def do_something(self):
        pass

    def __str__(self):
        return self._name + ", " + self._email

users = [User("Test", "test@dg.com"), User("Test2", "test2@dg.com")]

for user in users:
    user.do_something()
