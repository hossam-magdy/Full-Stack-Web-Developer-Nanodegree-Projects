import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, PROJECT_ROOT) # no import from local dir

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id              = Column(Integer, primary_key=True)
    id_at_provider  = Column(String(50), nullable=False)
    name            = Column(String(25))
    email           = Column(String(50))
    picture         = Column(String(500))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'email'        : self.email,
           'picture'      : self.picture,
       }

class Category(Base):
    __tablename__ = 'category'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(25), nullable = False)
    user_id     = Column(Integer,ForeignKey('user.id'))
    user        = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'      : self.user_id,
       }

class Item(Base):
    __tablename__ = 'menu_item'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(50), nullable = False)
    description = Column(String(500))
    cat_id      = Column(Integer,ForeignKey('category.id'))
    # the "ON DELETE CASCADE": http://docs.sqlalchemy.org/en/rel_0_9/orm/cascades.html
    cat         = relationship(Category, backref=backref('menu_item', cascade='all, delete'))
    user_id     = Column(Integer,ForeignKey('user.id'))
    user        = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'           : self.name,
           'description'    : self.description,
           'id'             : self.id,
           'cat_id'         : self.cat_id,
           'user_id'        : self.user_id,
       }


engine = create_engine('sqlite:///{}'.format(os.path.join(PROJECT_ROOT, 'itemCatalog.db')))

Base.metadata.create_all(engine)

