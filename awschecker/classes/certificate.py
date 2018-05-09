
import pytz
import logging
from .arn import AWSARN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime

Base = declarative_base()

# arn #timestamp #region #account #boto3client #metdata
class AWSCertificate():

    def __init__(self, pARN, DomainName, Status, CertificateTransparencyLoggingPreference, Serial):
        self.ARN = pARN
        self.DomainName = DomainName
        self.Status = Status
        self.CertificateTransparencyLoggingPreference = CertificateTransparencyLoggingPreference
        self.Serial = Serial
        self.timestamp = format(datetime.datetime.now(pytz.utc)
                                )

        myARN = AWSARN(self.ARN)
        self.Details = myARN

        url = "https://{}.console.aws.amazon.com/{}/home?region={}#/?id={}"
        self.url = url.format(
            myARN.region, myARN.service, myARN.region, myARN.resource)

    def __repr__(self):
        return str(self.__dict__)
