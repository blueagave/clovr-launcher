# coding=utf-8

from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, Markup
from flask_login import login_required, login_user, logout_user

from clovr_launcher import app
from clovr_launcher.user.models import User

blueprint = Blueprint('public', '__name__', static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    ## Likely need to change this for our use case...
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    ## Put logic here to handle logging in
    return render_template('public/login.html')


@blueprint.route('/logout')
@login_required
def logout():
    """Logout a user from the VM launcher application."""
    logout_user()
    return render_template('public/templates/logut.html')


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register a new user for the launcher app."""
    ## Put logic in here to handle registering new users.
    return render_template('public/register.html')

