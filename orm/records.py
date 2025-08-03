from collections import defaultdict
import inspect

from psycopg import sql

from .column import Column


class Meta(type):
    table_to_class_mapping = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if table := attrs.get('_table'):
            Meta.table_to_class_mapping[table] = cls
            if not hasattr(cls, '_triggers_to_methods_dict'):
                cls._triggers_to_methods_dict = defaultdict(list)
            for attr_value in attrs.values():
                if callable(attr_value) and hasattr(attr_value, '_triggers'):
                    for trigger in attr_value._triggers:
                        cls._triggers_to_methods_dict[trigger].append(attr_value)


class Records(metaclass=Meta):
    _table = None

    def __init__(self, cr, ids=()):
        self._cr = cr
        self._ids = ids

    def __iter__(self):
        for id in self._ids:
            yield type(self)(self._cr, (id, ))

    def create(self, col_value_dict):
        columns = sql.SQL(', ').join(map(sql.Identifier, col_value_dict.keys()))
        placeholders = sql.SQL(', ').join(map(sql.Placeholder, col_value_dict.keys()))
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(self._table),
            columns,
            placeholders,
        )
        self._cr.execute(query, col_value_dict)
        new_id = self._cr.fetchone()['id']
        new_record = type(self)(self._cr, (new_id, ))
        new_record.triggers(*col_value_dict.keys())
        return new_record

    def read(self, cols):
        query = sql.SQL("SELECT {} FROM {} WHERE id IN ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, cols)),
            sql.Identifier(self._table),
            sql.SQL(', ').join(sql.Placeholder() for _ in self._ids),
        )
        self._cr.execute(query, self._ids)
        return self._cr.fetchall()

    def update(self, vals):
        query = sql.SQL("UPDATE {} SET {} WHERE id IN ({})").format(
            sql.Identifier(self._table),
            sql.SQL(', ').join(sql.SQL('{} = {}').format(
                    sql.Identifier(col),
                    sql.Placeholder()
                ) for col in vals.keys()
            ),
            sql.SQL(', ').join(sql.Placeholder() for _ in self._ids),
        )
        self._cr.execute(query, (*vals.values(), *self._ids))
        self.triggers(*vals.keys())

    def delete(self):
        query = sql.SQL("DELETE FROM {} WHERE id IN ({})").format(
            sql.Identifier(self._table),
            sql.SQL(', ').join(sql.Placeholder() for _ in self._ids),
        )
        self._cr.execute(query, self._ids)

    def triggers(self, *cols):
        for col in cols:
            for method in self._triggers_to_methods_dict[col]:
                method(self)

    @classmethod
    def get_column_infos(cls):
        return {name: value.type for name, value in inspect.getmembers(cls) if isinstance(value, Column)}

    def ensure_one(self):
        if len(self._ids) != 1:
            raise Exception("Operation only allowed for recordset of len 1.")
