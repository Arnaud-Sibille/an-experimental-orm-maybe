from .column import Column

class Meta(type):
    table_to_class_mapping = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if table := attrs.get('_table'):
            Meta.table_to_class_mapping[table] = cls

class Records(metaclass=Meta):
    _table = None

    def __init__(self, cr, ids=()):
        self._cr = cr
        self._ids = ids

    def create(self, columns, values):
        query = f"""
            INSERT INTO {self._table} ({', '.join(columns)})
            VALUES {values}
            RETURNING id
        """
        self._cr.execute(query)
        new_id = self._cr.fetchone()['id']
        return type(self)(self._cr, (new_id, ))

    @classmethod
    def get_column_infos(cls):
        return {key: value.attrs for key, value in cls.__dict__.items() if isinstance(value, Column)}

    def ensure_one(self):
        if len(self._ids) != 1:
            raise Exception("Operation only allowed for recordset of len 1.")
