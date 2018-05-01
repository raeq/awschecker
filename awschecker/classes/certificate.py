
import pytz
import logging


from .util import parse_arn
from .arn import AWSARN


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime

Base = declarative_base()

# arn #timestamp #region #account #boto3client #metdata


class CertTable(Base):
    logger = logging.getLogger(__name__)
    __tablename__ = 'certificates'

    ARN = Column(String, primary_key=True)
    DomainName = Column(String)
    region = Column(String)
    account = Column(String)
    Status = Column(String)
    Serial = Column(String)
    timestamp = Column(TIMESTAMP)

    def __repr__(self):
        return "<Certificate(ARN='%s', \
        DomainName='%s', region='%s', account='%s',  \
        Status='%s', region='%s', Serial='%s')>" % (
            self.ARN, self.DomainName,
            self.region, self.account, self.password,
            self.Status, self.Serial)


class AWSCertificate():

    def __init__(self, pARN, DomainName, Status, CertificateTransparencyLoggingPreference, Serial):
        self.ARN = pARN
        self.DomainName = DomainName
        self.Status = Status
        self.CertificateTransparencyLoggingPreference = CertificateTransparencyLoggingPreference
        self.Serial = Serial
        self.Details = parse_arn(self.ARN)
        self.timestamp = format(datetime.datetime.now(pytz.utc)
                                )

        myARN = AWSARN(self.ARN)
        self.Details = myARN

        url = "https://{}.console.aws.amazon.com/{}/home?region={}#/?id={}"
        self.url = url.format(
            myARN.region, myARN.service, myARN.region, myARN.resource)

    def __repr__(self):
        return str(self.__dict__)
