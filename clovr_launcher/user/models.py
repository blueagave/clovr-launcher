# -*- coding: utf-8 -*-

import datetime as dt

from flask_login import UserMixin

from clovr_launcher.database import (Column, Model, SurrogatePK, db, 
                                     reference_col, relationship)
from clovr_launcher.extensions import bcrypt

class Credential(UserMixin, SurrogatePK, Model):
    """A pseudo-user for the CloVR-launcher app.

    A set of credentials simulates a user in a normal application by 
    serving as a way to switch between Amazon EC2 accounts without having 
    to provide username and passwords.

    For a credential the "password" is simulated by using AWS access key ID
    and AWS secret key."""
    __tablename__ = "credentials"

    password = Column(db.String(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    
    ## These are our app specific columns
    credential_name = Column(db.String(80), unique=True, nullable=False)
    aws_access_key = Column(db.String(20), unique=True, nullable=False)
    aws_secret_key = Column(db.String(40), unique=True, nullable=False)

    def __init__(self, credential_name, aws_access_key, aws_secret_key,
                 **kwargs):
        enc_access_key = bcrypt.generate_password_hash(aws_access_key)
        enc_secret_key = bcrypt.generate_password_hash(aws_secret_key)

        db.Model.__init__(self, 
                          credential_name=credential_name, 
                          authenticated = False,
                          aws_access_key=enc_access_key,
                          aws_secret_key=enc_secret_key,
                          password=enc_access_key + enc_secret_key,
                          **kwargs)
        
    def get_id(self):
        """Returns a unicode string that uniquely identifies this credential. 
        Because credential names are unqiue this will always return the 
        user-supplied credential."""
        return unicode(self.credential_name)

    def check_password(self, value):
        """Checks credential "password" -- a credentials password is 
        defined as the combination hashed secret key and access key and is 
        stored in the password field for each user."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represents instance as a unique string."""
        return "<Credential %r>" % self.credential_name
