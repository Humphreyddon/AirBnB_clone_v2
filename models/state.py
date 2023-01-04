#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    @property
    def cities(self):
        city_list = []
        cityL = list(storage.all(City).values())
        for city in cityL:
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
