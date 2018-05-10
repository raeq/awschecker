
import pytz
import logging
from .arn import AWSARN
from .awsobject import AWSObject
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


class AWSCertificate(AWSObject):

    def __init__(self, description):
        AWSObject.__init__(self, description['CertificateArn'])

        self.DomainName = description['DomainName']
        self.Status = description['Status']
        self.CertificateTransparencyLoggingPreference = description[
            'Options']['CertificateTransparencyLoggingPreference']

        if self.Status == 'PENDING_VALIDATION':
            self.Serial = ''
        else:
            self.Serial = description['Serial']

        self.timestamp = format(datetime.datetime.now(pytz.utc))

    def __repr__(self):
        return str(self.__dict__)
