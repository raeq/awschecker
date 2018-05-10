
import pytz
import logging
from .arn import AWSARN
from .awsobject import AWSObject
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
from boto3.session import Session
import boto3

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
        self.logger = logging.getLogger(__name__)
        AWSObject.__init__(self, description['CertificateArn'])

        self.DomainName = description['DomainName']
        self.Status = description['Status']
        self.Details = description
        self.CertificateTransparencyLoggingPreference = description[
            'Options']['CertificateTransparencyLoggingPreference']

        if self.Status == 'PENDING_VALIDATION':
            self.Serial = ''
            self.Issuer = ''
            self.Type = ''
        else:
            self.Serial = description['Serial']
            self.Issuer = description['Issuer']
            self.Type = description['Type']

        self.timestamp = format(datetime.datetime.now(pytz.utc))

    def disable_transparency_logging(self):

        if self.Issuer == 'Amazon' and self.Type == 'AMAZON_ISSUED':

            s = Session()
            acmclient = boto3.client('acm', region_name=self.ARN.region)

            response = acmclient.update_certificate_options(
                CertificateArn=self.ARN.arn,
                Options={
                    'CertificateTransparencyLoggingPreference': 'DISABLED'
                }
            )

            #response = acmclient.update_certificate_options(CertificateArn=self.ARN.arn, Options=mOptions)
            self.logger.warn(
                "Cert %s had cert tran logging disable successfully", self.url)

    def enable_transparency_logging(self):

        if self.Issuer == 'Amazon' and self.Type == 'AMAZON_ISSUED':

            s = Session()
            acmclient = boto3.client('acm', region_name=self.ARN.region)

            response = acmclient.update_certificate_options(
                CertificateArn=self.ARN.arn,
                Options={
                    'CertificateTransparencyLoggingPreference': 'ENABLED'
                }
            )

            #response = acmclient.update_certificate_options(CertificateArn=self.ARN.arn, Options=mOptions)
            self.logger.warn(
                "Cert %s had cert tran logging enabled successfully", self.url)

    def __repr__(self):
        return str(self.__dict__)
