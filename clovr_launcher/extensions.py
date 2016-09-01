# -*- coding: utf-8 -*-

from flask_bcrypt import Bcrypt
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
cache = Cache()
