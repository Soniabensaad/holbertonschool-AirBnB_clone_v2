#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from models import storage
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import getenv
    
class State(BaseModel, Base):
    """ State class """
    __tablename__ = "States"
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state')

if models.storage_type != "db":
    @property
    def cities(self):
        """FileStorage relationship between State and City"""
        list = []
        for city in storage.all(City):
            if (city.state_id == self.id):
                 list.append(city)
        return list

