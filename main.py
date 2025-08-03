import code
import configparser
import importlib

import psycopg

from orm import Meta, utils

CONFIG_FILE_NAME = ".config.ini"


def setup(cr):
    for record_class in Meta.table_to_class_mapping.values():
        utils.create_table_if_not_exists(cr, record_class._table)
        utils.create_columns_if_not_exist(cr, record_class)

def main(conn, cr):
    setup(cr)

    test_locals = execute_test_code(conn, cr)

    code.interact(local=locals() | test_locals)

def execute_test_code(conn, cr):
    def get_instance(table, ids=()):
        return Meta.table_to_class_mapping[table](cr, ids)

    partner = get_instance('partner')
    partner = partner.create({
        'name': "Yohan",
        'last_name': "Yoho",
        "favorite_color": "lightblue",
    })
    print(partner.read(['name', 'last_name', 'display_name', 'age', 'favorite_color']))
    partner.age = 14
    partner.update({'name': 'mmmh', 'last_name': 'chocolat'})
    print(partner.read(['name', 'last_name', 'display_name', 'age', 'favorite_color']))

    dinosaur = get_instance('dinosaur')
    dinosaur = dinosaur.create({
        'name': "T-Rex",
    })
    print(dinosaur.name)

    conn.commit()

    return locals()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)

    for addon in config['framework']['addons'].split(','):
        importlib.import_module(f"addons.{addon}")

    dbname = config['postgres']['dbname']
    utils.create_db_if_not_exists(dbname)

    with psycopg.connect(dbname=dbname) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cr:
            main(conn, cr)
