from orm import Column, Records, register_as_triggered

class Partner(Records):
    _table = 'partner'

    name = Column("TEXT")
    last_name = Column("TEXT")
    display_name = Column("TEXT")

    @register_as_triggered('name', 'last_name')
    def compute_display_name(self):
        for partner in self:
            partner.display_name = f'{partner.name} {partner.last_name}'
