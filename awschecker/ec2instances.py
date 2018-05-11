
import boto3
#from awschecker.classes import certificate
from boto3.session import Session
import logging
from .classes import EC2Instance
from .classes import AWSARN
from .decorator_logging import logged
import constants

def check_items():
    """Queries AWS regions for ACM certificates, and then checks them."""

    logger = logging.getLogger(__name__)
    logger.debug("Begin searching for instances.")
    s = Session()

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
                check_one_item(myinst)

    logger.debug("End searching for instances.")


@logged(logging.DEBUG)
def check_one_item(anitem):
    """Takes a certificate object, and performs validation checks."""

    logger = logging.getLogger(__name__)
    logger.debug(anitem)
