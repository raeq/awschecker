
import pytz
import logging
from .arn import AWSARN
import datetime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, TIMESTAMP


class AWSObject():
    def __init__(self, pARN):

        self.ARN = AWSARN(pARN)
        url = "https://{}.console.aws.amazon.com/{}/home?region={}#/?id={}"

        self.url = url.format(
            self.ARN.region, self.ARN.service, self.ARN.region, self.ARN.resource)

    def __repr__(self):
        return str(self.__dict__)