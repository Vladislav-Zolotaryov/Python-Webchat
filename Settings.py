import os
from sqlalchemy.engine.url import URL

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']