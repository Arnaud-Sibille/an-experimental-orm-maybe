import psycopg
from psycopg import sql

DEFAULT_DATABASE_NAME="postgres"


def create_db_if_not_exists(dbname):
    with psycopg.connect(dbname=DEFAULT_DATABASE_NAME, autocommit=True) as conn:
        with conn.cursor() as cr:
            cr.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname, ))
            if not cr.fetchone():
                cr.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

def create_table_if_not_exists(cr, record_class):
    col_infos = {
        "id": "SERIAL PRIMARY KEY",
        **record_class.get_column_infos(),
    }
    cols_sql = sql.SQL(', ').join(
       sql.SQL("{} {}").format(
           sql.Identifier(name),
           sql.SQL(type),
       ) for name, type in col_infos.items()
    )
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(record_class._table),
        cols_sql,
    )
    cr.execute(query)
