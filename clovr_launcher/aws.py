# -*- coding: utf-8 -*-

"""
aws.py
~~~~~~

Collection of functions that facilitate interaction between AWS (specifically
EC2) and our app.
"""

import boto3
import botocore

from flask import current_app, abort


def _connect(access_key, secret_key):
    """Opens a connection to the Amazon's EC2 service and returns a boto3
    client.

    :param secret_key: AWS secret access key 
    :param access_key: AWS access key 
    """
    return boto3.resource('ec2',
                           region_name='us-east-1',
                           aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key)


def get_clovr_amis(access_key, secret_key):
    """Retrieves a list of AMI name and AMI ID's for all valid CloVR VM's on
    the us-east-1 region.
    """
    response = {}
    try:
        client = _connect(access_key, secret_key)
        
        for image in client.images.filter(Filters=[{'Name': 'name', 'Values': ['clovr-standard*']}]).all():
            response.setdefault('amis', []).append({'name': image.name, 'id': image.id})

        response['amis'].reverse()
        response['success'] = True
    except botocore.exceptions.ClientError as ce:
        response['success'] = False
        response['message'] = ce

    return response


def validate_credentials(access_key, secret_key):
    """Verifies whether or not the supplied secret key and access key are
    valid. 
    """
    valid = True

    try:
        client = _connect(access_key, secret_key)

        for i in client.instances.all(): print(i)
    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "AuthFailure":
            valid = False

    return valid


def _format_date(date):
    """Formats date to a more readable format for display

    :param date: datetime object
    :rtype: string
    """
    return date.strftime("%m-%d-%y %H:%M:%S %Z")
    

def list_instances(access_key, secret_key, instance_id=[]):
    """Lists instances associated with the AWS access key and secret acccess
    key.

    :param secret_key: AWS secret access key
    :param access_key: AWS access key
    :instance_id: A list containing specific instances to retrieve status of
    :rtype: dict
    """
    response = {}
    instances = []

    try:
        client = _connect(access_key, secret_key)

        for instance in client.instances.filter(InstanceIds=instance_id).all():
            instances.append({'id': instance.id,
                              'name': instance.image.name,
                              'state': instance.state.get('Name'),
                              'instance_type': instance.instance_type,
                              'address': instance.public_ip_address,
                              'start_time': _format_date(instance.launch_time)
                             })

        response['success'] = True
        response['instances'] = instances
    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "InvalidInstanceID.Malformed":
            response['success'] = "False"
            response['message'] = "Instance ID does not exist or is malformed."
            pass

    return response


def _create_clovr_security_group(client, enable_ssh=False):
    """Creates a security group to ensure that port 80 (and port 22 if needed)
    are open on any CloVR EC2 innstance.

    :param client: boto EC2 client
    :param enable_ssh: True/False to open up access to port 22 
    :rtype: None
    """
    sec_group = client.create_security_group(GroupName='clovr', 
                                             Description='Ports required to run CloVR on EC2')
    sec_group.authorize_ingress(IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp='0.0.0.0/0')
    
    if enable_ssh:
        sec_group.authorize(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp='0.0.0.0/0')


def start_instances(access_key, secret_key, ami_id, instance_type, num_instances=1):
    """Starts one or more instances with the provided AMI ID and instance type.

    :param secret_key: AWS secret access key
    :param access_key: AWS access key
    :param ami_id: Amazon Machine ID
    :param instance_type: EC2 instance type
    :param num_instances: Number of instances to start
    :rtype: dict
    """
    response = {}

    try:
        client = _connect(access_key, secret_key)

        ## We need to check if a security group that has the port for HTTP 
        ## open exists and if not create it.
        sec_groups = client.security_groups.filter(Filters=[{"Name": "group-name",
                                                             "Values": ["clovr"]}])
        if not sec_groups:
            _create_clovr_security_group(client)
        
        instances = client.create_instances(ImageId=ami_id, 
                                            MinCount=num_instances,
                                            MaxCount=num_instances,
                                            InstanceType=instance_type)
        response['success'] = True
        response['instances'] = [instance.id for instance in instances]
    except botocore.exceptions as be:
        raise Exception(500, be.msg)

    return response


def terminate_instances(secret_key, access_key, instance_ids):
    """Terminates all specified instance.

    :param secret_key: AWS secret access key
    :param access_key: AWS access key
    :param instance_ids: A list of all instance ID's to be terminated
    :rtype: dict
    """
    response = {}

    try:
        client = _connect(secret_key, access_key)
        instances = client.instances.filter(InstanceIds=instance_ids).terminate()
        response['status'] = "ok"
        response['instances'] = instances
    except botocore.exceptions.ClientError as ce:
        pass

    return response
