"""
Gethers all ec2 instances from an account.
Can optionally check them against rules.
"""
import logging
import boto3
import constants
from pprint import pprint
from .decorator_logging import logged
from .classes import EC2Instance


@logged(logging.DEBUG)
def check_items():
    """Entry point. Is called to both gather objects and to check them."""
    map(check_one_item, gather_instances())
    for i in gather_instances():
        check_one_item(i)


@logged(logging.DEBUG)
def gather_instances():
    """Queries AWS regions for EC2 instances, and returns a list of them."""

    logger = logging.getLogger(__name__)
    logger.debug("Begin searching for instances.")

    allinstances = []
    for region in constants.PREFERRED_REGIONS:
        logger.debug("Searching region: %s", region)

        ec2 = boto3.resource('ec2', region_name=region)
        for i in (ec2.instances.all()):
            allinstances.append(i)

    logger.debug("End searching for instances.")
    return allinstances


@logged(logging.DEBUG)
def check_one_item(anitem):
    """Takes an EC2 instance object, and performs validation checks."""

    logger = logging.getLogger(__name__)