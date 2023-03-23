#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, INTEGER, Float, Table
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship
from os import getenv
storage = getenv("HBNB_TYPE_STORAGE")
if storage == 'db':
    metadata = Base.metadata
    place_amenity = Table("place_amenity", metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if storage == 'db':
        city_id = Column(String(60),  ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60),  ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(INTEGER, nullable=False, default=0)
        number_bathrooms = Column(INTEGER, nullable=False, default=0)
        max_guest = Column(INTEGER, nullable=False, default=0)
        price_by_night = Column(INTEGER, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship(
            'Review', cascade="all, delete-orphan", backref='place')
        amenities = relationship(
            'Amenity',  secondary="place_amenity", viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
    
        

    if storage != 'db':
        @property
        def reviews(self):
            lis = []
            for i in self.__session.query(Review).all():
                if (i.Place_id == self.id):
                    lis.append(i)
            return (lis)

        @property
        def amenities(self):
            lis = []
            for i in self.__session.query(Amenity).all():
                if (i.amenity_ids == self.id):
                    lis.append(i)
            return (lis)
