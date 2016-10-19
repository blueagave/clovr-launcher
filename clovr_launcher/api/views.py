# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, abort, request
from flask_login import login_required, current_user

from clovr_launcher.aws import start_instances, terminate_instances, list_instances, get_clovr_amis


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@blueprint.errorhandler(Exception)
def handle_server_error(error):
    response = jsonify({
        'success': False,
        'message': str(error),
        'status_code': 500
    })

    return response, 500


@blueprint.route('/ami/', methods=['GET'])
def get_ami_ids():
    """Retrieves a list of all AMI names and AMI ID's for all CloVR images
    currently found on the us-east-1 region of EC2."""
    resp = get_clovr_amis(current_user.aws_access_key, current_user.aws_secret_key)
    return jsonify(resp)


@blueprint.route('/instances/', methods=['GET'])
@login_required
def get_instances():
    """Retrieves all instances for the currently logged in user."""
    resp = list_instances(current_user.aws_access_key, current_user.aws_secret_key)

    if not resp.get('success'):
       abort(500)

    return jsonify(resp)


@blueprint.route('/instances/<string:instance_id>', methods=['GET'])
@login_required
def get_instance(instance_id):
    """Retrieves a specific EC2 instance provided an EC2 instance ID for the 
    currently logged in user."""
    resp = list_instances(current_user.aws_access_key,
                          current_user.aws_secret_key,
                          [instance_id])

    return jsonify(resp)        


@blueprint.route('/instances/', methods=['POST'])
@login_required
def start_instance():
    """Launches an EC2 instance with the provided information from the user:
            {
                ami_id: <EC2 AMI ID>
                num_instances: <NUMBER OF INSTANCES TO LAUNCH>
                security_group: <NAME OF SECURITY GROUP TO USE>
            }
    """
    resp = start_instances(current_user.aws_access_key, 
                           current_user.aws_secret_key,
                           request.form.get('ami_id'),
                           request.form.get('instance_type'))
    
    return jsonify(resp)


@blueprint.route('/instances/', methods=['DELETE'])
@login_required
def terminate_instances():
    """Terminates all current running EC2 instances for the logged in user."""
    pass


@blueprint.route('/instances/<string:instance_id>', methods=['DELETE'])
@login_required
def terminate_instance(instance_id):
    """Terminates a specific EC2 instance provided an EC2 instance ID."""
    pass
