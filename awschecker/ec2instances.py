"""
Gethers all ec2 instances from an account.
Can optionally check them against rules.
"""
import logging
import boto3
import constants
from .decorator_logging import logged
from .classes import EC2Instance


@logged(logging.DEBUG)
def check_items():
    """Entry point. Is called to both gather objects and to check them."""
    for cert in gather_instances():
        check_one_item(cert)


@logged(logging.DEBUG)
def gather_instances():
    """Queries AWS regions for EC2 instances, and returns a list of them."""

    logger = logging.getLogger(__name__)
    logger.debug("Begin searching for instances.")
    allinstances = []

    for region in constants.PREFERRED_REGIONS:
        logger.debug("Searching region: %s", region)

        client = boto3.client('ec2', region_name=region)
        ec2 = boto3.resource('ec2',region_name=region)
        response_iterator = client.get_paginator(
            'describe_instances').paginate()

        for p in response_iterator:
            for i in p['Reservations']:
                for j in i['Instances']:
                    myinst = ec2.Instance(j['InstanceId'])
                    allinstances.append(myinst)

    logger.debug("End searching for instances.")
    return allinstances


@logged(logging.DEBUG)
def check_one_item(anitem):
    """Takes an EC2 instance object, and performs validation checks."""

    logger = logging.getLogger(__name__)
