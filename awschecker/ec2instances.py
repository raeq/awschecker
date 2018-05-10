
import boto3
#from awschecker.classes import certificate
from boto3.session import Session
import logging
from .classes import EC2Instance
from .classes import AWSARN


def check_items():
    """Queries AWS regions for ACM certificates, and then checks them."""

    logger = logging.getLogger(__name__)
    logger.info("Begin searching for instances.")
    s = Session()

    for region in s.get_available_regions('ec2'):
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
                check_one_item(myinst)

    logger.info("End searching for instances.")


def check_one_item(anitem):
    """Takes a certificate object, and performs validation checks."""

    logger = logging.getLogger(__name__)
    logger.debug(anitem)
