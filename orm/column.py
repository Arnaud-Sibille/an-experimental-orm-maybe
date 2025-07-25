class Column:
    def __init__(self, attrs):
        self.attrs = attrs

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        instance.ensure_one()

        query = f"SELECT {self.name} FROM {instance._table} WHERE id = {instance._ids[0]}"
        instance._cr.execute(query)
        return instance._cr.fetchone()[self.name]
