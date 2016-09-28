# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def account_view():
    """A view containing account details for the users"""
    pass
