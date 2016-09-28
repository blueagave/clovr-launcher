# -*- coding: utf-8 -*-

"""Login forms"""

from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length

from clovr_launcher.user.models import User


class LoginForm(Form):
    """A form containings parameters required for a "user" to login to the 
    CloVR launcher app"""

    username = StringField('Username', 
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'User Name'})
    password = PasswordField('Password', 
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})

    def __init__(self, *args, **kwargs):
        """Create LoginForm instance"""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate LoginForm"""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True
