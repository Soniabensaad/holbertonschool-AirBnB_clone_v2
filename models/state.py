#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models.city import City
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city = relationship("City", cascade="all, delete", backref="state")


    if models.storage_type != "db":
        @property
        def cities(self):
            """getter for cities that return
            a list of city instance equale to
            curent state id
            """
            list_city = []
            inst = models.storage.all(City)
            for value in inst.values():
                if value.state_id == self.id:
                    list_city.append(value)
            return list_city