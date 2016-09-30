# -*- coding: utf-8 -*-

"""User forms."""

from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length

from clovr_launcher.aws import validate_credentials

from .models import User


class RegisterForm(Form):
    """A form containing parameters required to register an account for user  
    on the CloVR launcher app."""

    username = StringField('User Name', 
                           validators=[DataRequired(), Length(min=3, max=60)], 
                           render_kw={'placeholder': 'User Name'})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=100)],
                             render_kw={'placeholder': 'Password'})
    confirm = PasswordField('Verify Password',
                            validators=[DataRequired(), 
                                        EqualTo('password', message='Passwords must match.')],
                            render_kw={'placeholder': 'Verify Password'})
    access_key = StringField('AWS Access Key ID',
                             validators=[DataRequired(), Length(min=20, max=25)],
                             render_kw={'placeholder': 'AWS Access Key'})
    secret_key = StringField('AWS Secret Access Key',
                             validators=[DataRequired(), Length(min=40, max=45)],
                             render_kw={'placeholder': 'AWS Secret Access Key'})

    def __init__(self, *args, **kwargs):
        """Create instance of registration form."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate registration form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User name already exists')
            return False

        if not validate_credentials(self.access_key.data, self.secret_key.data):
            self.access_key.errors.append('Invalid AWS Access Key')
            self.secret_key.errors.append('Invalid AWS Secret Access Key')
            return False

        return True
