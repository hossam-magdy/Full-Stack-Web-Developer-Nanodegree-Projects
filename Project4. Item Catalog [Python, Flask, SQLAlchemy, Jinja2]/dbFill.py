import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, PROJECT_ROOT) # no import from local dir

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dbSetup import Base, Category, Item, User
import random, string, httplib2, json, requests

engine = create_engine('sqlite:///{}'.format(os.path.join(PROJECT_ROOT, 'itemCatalog.db')))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def rndm(length=5):
    return ''.join(random.choice(string.letters + " ") for x in range(length))

newCategory = Category(user_id = 1, name = "Cat-{}".format(rndm()))
session.add(newCategory)
session.commit()
print "Added cat, id={}".format(newCategory.id)

newItem = Item(user_id = 1, cat_id = newCategory.id, name = "Item-{}".format(rndm()), description = rndm(20))
session.add(newItem)
session.commit()
print "Added item, id={}".format(newItem.id)

newItem = Item(user_id = 1, cat_id = newCategory.id, name = "Item-{}".format(rndm()), description = rndm(20))
session.add(newItem)
session.commit()
print "Added item, id={}".format(newItem.id)

newItem = Item(user_id = 1, cat_id = newCategory.id, name = "Item-{}".format(rndm()), description = rndm(20))
session.add(newItem)
session.commit()
print "Added item, id={}".format(newItem.id)

newItem = Item(user_id = 1, cat_id = newCategory.id, name = "Item-{}".format(rndm()), description = rndm(20))
session.add(newItem)
session.commit()
print "Added item, id={}".format(newItem.id)


