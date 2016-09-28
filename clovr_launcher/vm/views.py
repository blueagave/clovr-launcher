# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, Markup
from flask_login import login_required


blueprint = Blueprint('vm', __name__, url_prefix='/vm', static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def start_vm():
    """Landing page to launch a CloVR VM. Allows user to select what kind of 
    EC2 instance they'd like to launch as well as the number of instances to
    launch."""
    return render_template('vm/start_vm.html')


@blueprint.route('/manage/', methods=['GET'])
@login_required
def manage_vms():
    return render_template('vm/manage_vms.html')
