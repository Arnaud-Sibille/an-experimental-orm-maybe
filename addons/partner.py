from orm import Column, Records

class Partner(Records):
    _table = 'partner'

    name = Column("TEXT")
    last_name = Column("TEXT")
