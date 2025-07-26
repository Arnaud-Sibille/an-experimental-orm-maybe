from psycopg import sql


class Column:
    def __init__(self, attrs):
        self.attrs = attrs

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        instance.ensure_one()

        query = sql.SQL("SELECT {} FROM {} WHERE id = %s").format(
            sql.Identifier(self.name),
            sql.Identifier(instance._table),
        )
        instance._cr.execute(query, instance._ids)
        return instance._cr.fetchone()[self.name]
