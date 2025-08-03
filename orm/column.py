class Column:
    def __init__(self, type):
        self.type = type

    def __set_name__(self, _owner, name):
        self.name = name

    def __get__(self, instance, _owner):
        instance.ensure_one()

        return instance.read([self.name])[0][self.name]

    def __set__(self, instance, value):
        instance.update({self.name: value})
