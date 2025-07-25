from .column import Column

def create_table_if_not_exist(cr, record_class):
    col_infos = {
        "id": "SERIAL PRIMARY KEY",
        **record_class.get_column_infos(),
    }
    cols_sql = ', '.join(f'{name} {attrs}' for name, attrs in col_infos.items())
    query = f"CREATE TABLE IF NOT EXISTS {record_class._table} ({cols_sql})"
    cr.execute(query)
