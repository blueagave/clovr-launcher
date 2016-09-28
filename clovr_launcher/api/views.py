# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required, current_user

from clovr_launcher.aws import start_instances, terminate_instances, list_instances


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@login_required
@blueprint.route('/instances/', methods=['GET'])
def get_instances():
    """Retrieves all instances for the currently logged in user."""
    resp = list_instances(current_user.aws_access_key, current_user.aws_secret_key)

    if resp.get('status') != "ok":
       abort(500)

    return jsonify(resp)


@login_required
@blueprint.route('/instances/<string:instance_id>', methods=['GET'])
def get_instance(instance_id):
    """Retrieves a specific EC2 instance provided an EC2 instance ID for the 
    currently logged in user."""
    resp = list_instances(current_user.aws_access_key,
                          current_user.aws_secret_key,
                          instance_id)

    if resp.get('status') != "ok":
        abort(500)

    return jsonify(resp)        


@login_required
@blueprint.route('/instances/', methods=['POST'])
def start_instance():
    """Launches an EC2 instance with the provided information from the user:
            {
                ami_id: <EC2 AMI ID>
                num_instances: <NUMBER OF INSTANCES TO LAUNCH>
                security_group: <NAME OF SECURITY GROUP TO USE>
            }
    """
    pass


@login_required
@blueprint.route('/instances/', methods=['DELETE'])
def terminate_instances():
    """Terminates all current running EC2 instances for the logged in user."""
    pass


@login_required
@blueprint.route('/instances/<string:instance_id>', methods=['DELETE'])
def terminate_instance(instance_id):
    """Terminates a specific EC2 instance provided an EC2 instance ID."""
    pass
