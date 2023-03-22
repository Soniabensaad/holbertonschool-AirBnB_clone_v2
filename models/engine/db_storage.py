#!/usr/bin/python3
"""new storage"""
from os import getenv
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage():
    """storage for datas"""
    __engine = None
    __session = None

    def __init__(self):
        """environment"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
              HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                  HBNB_MYSQL_DB),
            pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query database session"""
        dict = {}
        for q in classes:
            if cls is None :
                objs = self.__session.query(classes[q]).all()
                for value in objs:
                    key = value.__class__.__name__ + '.' + value.id
                    dict[key] = value
        return (dict)

    def new(self, obj):
        """add new object"""
        if obj is not None:
            self.__session.add(obj)
            self.save()

    def save(self):
        """save datas"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj if exists"""
        if obj is not None:
            del obj
            self.save()

    def reload(self):
        """reload object"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()