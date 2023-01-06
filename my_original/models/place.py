#!/usr/bin/python3

""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models import storage


association_table = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        reviews = relationship('Review', backref='place', cascade='delete')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities',
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ returns the list of Review instances with place_id
            equals to the current Place.id """
            review_list = []
            rev = storage.all(Review)
            for key, val in rev.items():
                if val.place_id == self.id:
                    review_list.append(val)
            return review_list

        @property
        def amenities(self):
            """ returns the list of Amenity instances based on the attribute
            amenity_ids that contain all Amenity.id linked to the Place"""
            amenity_list = []
            for amenity in list(storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
