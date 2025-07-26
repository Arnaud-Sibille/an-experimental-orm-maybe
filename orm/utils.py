from psycopg import sql


def create_table_if_not_exist(cr, record_class):
    col_infos = {
        "id": "SERIAL PRIMARY KEY",
        **record_class.get_column_infos(),
    }
    cols_sql = sql.SQL(', ').join(
       sql.SQL("{} {}").format(
           sql.Identifier(name),
           sql.SQL(attrs),
       ) for name, attrs in col_infos.items()
    )
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(record_class._table),
        cols_sql,
    )
    cr.execute(query)
