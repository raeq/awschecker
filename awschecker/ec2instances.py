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
        response = client.describe_instances()

        for reservation in response.get("Reservations"):
            for instance in reservation['Instances']:
                myinst = EC2Instance(description=instance, partition='aws',
                                     service='ec2', region=region,
                                     account=boto3.client(
                                         'sts').get_caller_identity().get('Account'),
                                     resourcetype='instance', resource=instance['InstanceId'])
                allinstances.append(myinst)

    logger.debug("End searching for instances.")
    return allinstances


@logged(logging.DEBUG)
def check_one_item(anitem):
    """Takes an EC2 instance object, and performs validation checks."""

    logger = logging.getLogger(__name__)
    logger.info(anitem)
