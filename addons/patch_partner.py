from orm import Column, Meta

table = 'partner'
class PartnerPatch(Meta.table_to_class_mapping[table]):
    _table = table

    favorite_color = Column("TEXT")
    age = Column("INTEGER")
