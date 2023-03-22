#!/usr/bin/python3
"""
DBstorage using sqlAlchemy
"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

class DBStorage:
    """using sqlAlchemy store datas"""
    __engine = None
    __session = None
    classes = ["State", "City", "User", "Place", "Review"]
    def __init__(self):
        """create the engine"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{database}", pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        dict = {}
        if cls is None:
            for q in self.classes:
                q = eval(q)
                for objet in self.__session.query(q).all():
                    key = objet.__class__.__name__ + "." + objet.id
                    dict[key] = objet
    
        else:
            for objet in self.__session.query(cls).all():
                key = objet.__class__.__name__ + "." + objet.id
                dict[key] = objet
        return dict
    
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj is not None:
            self.__session.delete(obj)
    def reload(self):
        """database (feature of SQLAlchemy"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory )
        self.__session = Session()
        



