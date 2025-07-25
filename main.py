#! /home/odoo/venvs/an_orm/bin/python
import code

import psycopg2
from psycopg2.extras import RealDictCursor

from orm import Meta, utils
import addons

DATABASE_NAME = "an_orm_db"

def setup(cr):
    for record_class in Meta.table_to_class_mapping.values():
        utils.create_table_if_not_exist(cr, record_class)

def main(conn, cr):
    def get_instance(table, ids=()):
        return Meta.table_to_class_mapping[table](cr, ids)

    setup(cr)

    # testing code
    partner = get_instance('partner')
    partner = partner.create(('name', 'last_name'), ('Some', 'One'))
    print(partner.name)
    print(partner.last_name)
    conn.commit()

    code.interact(local=locals())

if __name__ == '__main__':
    with psycopg2.connect(database=DATABASE_NAME) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cr:
            main(conn, cr)
