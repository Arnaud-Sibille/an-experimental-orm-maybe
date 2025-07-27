import psycopg
from psycopg import sql

DEFAULT_DATABASE_NAME="postgres"


def create_db_if_not_exists(dbname):
    with psycopg.connect(dbname=DEFAULT_DATABASE_NAME, autocommit=True) as conn:
        with conn.cursor() as cr:
            cr.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname, ))
            if not cr.fetchone():
                cr.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

def create_table_if_not_exists(cr, table):
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY)").format(
        sql.Identifier(table),
    )
    cr.execute(query)

def create_columns_if_not_exist(cr, record_class):
    for col_name, col_type in record_class.get_column_infos().items():
        query = sql.SQL("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} {}").format(
            sql.Identifier(record_class._table),
            sql.Identifier(col_name),
            sql.SQL(col_type),
        )
        cr.execute(query)
