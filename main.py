import code
import configparser

import psycopg

from orm import Meta, utils
import addons


def setup(cr):
    for record_class in Meta.table_to_class_mapping.values():
        utils.create_table_if_not_exists(cr, record_class)

def main(conn, cr):
    def get_instance(table, ids=()):
        return Meta.table_to_class_mapping[table](cr, ids)

    setup(cr)

    # testing code
    partner = get_instance('partner')
    partner = partner.create({
        'name': "Yohan",
        'last_name': "Yoho",
    })
    print(partner.name)
    print(partner.last_name)

    dinosaur = get_instance('dinosaur')
    dinosaur = dinosaur.create({
        'name': "T-Rex",
    })
    print(dinosaur.name)

    conn.commit()

    code.interact(local=locals())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(".config")
    dbname = config['postgres']['dbname']
    utils.create_db_if_not_exists(dbname)
    with psycopg.connect(dbname=dbname) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cr:
            main(conn, cr)
