# -*- coding: utf-8 -*-

from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from random import SystemRandom

from flask_login import UserMixin

from sqlalchemy.ext.hybrid import hybrid_property

from clovr_launcher.database import (Column, Model, SurrogatePK, db, 
                                     reference_col, relationship)


class User(UserMixin, SurrogatePK, Model):
    """A pseudo-user for the CloVR-launcher app.

    A set of credentials simulates a user in a normal application by 
    serving as a way to switch between Amazon EC2 accounts without having 
    to provide username and passwords.

    For a credential the "password" is simulated by using AWS access key ID
    and AWS secret key."""
    __tablename__ = "users"

    username = Column(db.String(80), unique=True, nullable=False)
    _password = Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))
    
    ## These are our app specific columns
    aws_access_key = Column(db.String(20), unique=True, nullable=False)
    aws_secret_key = Column(db.String(40), unique=True, nullable=False)

    def __init__(self, username, password, aws_access_key, aws_secret_key,
                 **kwargs):

        db.Model.__init__(self, 
                          username=username,
                          aws_access_key=aws_access_key,
                          aws_secret_key=aws_secret_key,
                          password=password,
                          **kwargs)
 
    @hybrid_property
    def password(self):
        return self._password

    @password.setter       
    def password(self, value):
        """Custom password setter that leverages the pbkdf2 algorithm for 
        hashing."""
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        
        self._password = self._hash_password(value)
       
    def _hash_password(self, password):
        """Hashes the provided password using the pbkdf2 algorithm."""
        pwd = password.encode('utf-8')
        salt = bytes(self._salt)
        buff = pbkdf2_hmac('sha512', pwd, salt, iterations=100000)
        return bytes(buff)

    def check_password(self, value):
        """Ensures that the provided password is valid."""
        new_hash = self._hash_password(value)
        return compare_digest(new_hash, self._password)

    def __repr__(self):
        """Represents instance as a unique string."""
        return "<User %r>" % self.username
