
import logging
from .awsobject import AWSObject
from ..decorator_logging import logged


@logged(logging.DEBUG)
class EC2Instance(AWSObject):
    """Represents an AWS EC2 Instance object."""

    def __init__(self, description='', partition='', service='', region='',
                 account='', resourcetype='', resource=''):
        """Constructor for an AWS EC@ virtual machine instance object.
            Args:
                description: String of the JSON object returned from describe_instance
            Returns:
                An EC2Instance object instantiated from the raw JSON.
        """
        self.logger = logging.getLogger(__name__)
        self.description = description

        super(__class__, self).__init__(partition=partition,
                                        service=service,
                                        region=region,
                                        account=account,
                                        resourcetype=resourcetype, resource=resource)
        self.logger.debug(self)
