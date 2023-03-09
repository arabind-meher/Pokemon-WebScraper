from sqlalchemy import Column, Integer, Float, String

from database import Base


class PokemonDB(Base):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False)
    form = Column(String(40))
    type_1 = Column(String(10))
    type_2 = Column(String(10))
    species = Column(String(40))
    height = Column(Float)
    weight = Column(Float)
    ability_1 = Column(String(25))
    ability_2 = Column(String(25))
    ability_h = Column(String(25))
    hp = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    sp_attack = Column(Integer)
    sp_defence = Column(Integer)
    speed = Column(Integer)
    total = Column(Integer)
