
import pytz
import logging
from .arn import AWSARN
import datetime
import pytz
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, TIMESTAMP


class AWSObject():
    """
    Superclass for all AWS object representations.
    Contains an see:ARN object, and has a URL attribute.
    """

    def __init__(self, *args, **kwargs):

        self.logger = logging.getLogger(__name__)
        self.timestamp = format(datetime.datetime.now(pytz.utc))

        if len(kwargs) <1:

            self.ARN = AWSARN(args[0])

        else:
            self.timestamp = format(datetime.datetime.now(pytz.utc))
            self.ARN = AWSARN (
                partition   =   kwargs.get('partition'),
                service=kwargs.get('service'),
                region=kwargs.get('region'),
                account=kwargs.get('account'),
                resourcetype=kwargs.get('resourcetype'),
                resource=kwargs.get('resource')
                    )

        url = "https://{}.console.aws.amazon.com/{}/home?region={}#/?id={}"

        self.url = url.format(
            self.ARN.region, self.ARN.service, self.ARN.region, self.ARN.resource)



    def __repr__(self):
        return str(self.__dict__)
