# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, Markup
from flask_login import login_required


blueprint = Blueprint('vm', __name__, url_prefix='/vms', static_folder='../static')


@blueprint.route('/')
@login_required
def start_vm():
    return render_template('start_vm.html')


@login_required
@blueprint.route('/manage')
def manage_vms():
    return render_template('manage_vms.html')
