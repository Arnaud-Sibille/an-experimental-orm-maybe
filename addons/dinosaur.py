from orm import Column, Records

class Dinosaur(Records):
    _table = 'dinosaur'

    name = Column("TEXT")
