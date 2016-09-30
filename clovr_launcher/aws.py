# -*- coding: utf-8 -*-

"""
aws.py
~~~~~~

Collection of functions that facilitate interaction between AWS (specifically
EC2) and our app.
"""

import boto3
import botocore

from flask import current_app


def _connect(secret_key, access_key):
    """Opens a connection to the Amazon's EC2 service and returns a boto3
    client.

    :param secret_key: AWS secret access key 
    :param access_key: AWS access key 
    """
    return boto3.resource('ec2',
                           region_name='us-east-1',
                           aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key)


def validate_credentials(secret_key, access_key):
    """Verifies whether or not the supplied secret key and access key are
    valid. 
    """
    client = _connect(access_key, secret_key)
    valid = True

    try:
        for i in client.instances.all(): print(i)
    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "AuthFailure":
            valid = False

    return valid


def list_instances(secret_key, access_key,instance_id=[]):
    """Lists instances associated with the AWS access key and secret acccess
    key.

    :param secret_key: AWS secret access key
    :param access_key: AWS access key
    :instance_id: A list containing specific instances to retrieve status of
    :rtype: dict
    """
    response = {}
   
    try:
        #client = _connect(secret_key, access_key)
        client = _connect(access_key, secret_key)

        instances = client.instances.filter(InstanceIds=instance_id)
        response['status'] = "ok"
        raise Exception('xyz')
        response['instances'] = instances
    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "InvalidInstanceID.Malformed":
            response['status'] = "error"
            response['message'] = "Instance ID does not exist or is malformed."
            pass

    return response


def start_instances(secret_key, access_key, ami_id, instance_type, num_instances=1):
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
        client = _connect(secret_key, access_key)

        instances = client.create_instances(ImageId=ami_id, 
                                            SecurityGroups=['clovr'],
                                            MinCount=num_instances,
                                            MaxCount=num_instances,
                                            InstanceType=instance_type)
        response['status'] = "ok"
        response['instances'] = instances
    except botocore.exceptions.ClientError as ce:
        pass

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
