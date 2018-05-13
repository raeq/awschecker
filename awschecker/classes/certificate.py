
import logging
from .awsobject import AWSObject

# arn #timestamp #region #account #boto3client #metdata


class AWSCertificate(AWSObject):
    """Represents an AWS ACM certificate object."""

    def __init__(self, description=''):
        """Constructor for an AWS certificate object.and
            Args:
                description: String of the JSON object returned from
                describe_certificate
            Returns:
                An AWSCertificate object instantiated from the raw JSON.
        """
        self.logger = logging.getLogger(__name__)
        super(__class__, self).__init__(description
                                        ['CertificateArn'])

        self.DomainName = description['DomainName']
        self.Status = description['Status']
        self.Details = description
        self.CertificateTransparencyLoggingPreference = description[
            'Options']['CertificateTransparencyLoggingPreference']

        if self.Status in ['PENDING_VALIDATION', 'VALIDATION_TIMED_OUT']:
            self.Serial = ''
            self.Issuer = ''
            self.Type = ''
        else:
            self.Serial = description['Serial']
            self.Issuer = description['Issuer']
            self.Type = description['Type']

        self.logger.debug(self)

    def disable_transparency_logging(self):
        """Classmethod to disable certificate transparency
        logging on this certificate"""

        if self.Issuer == 'Amazon' and self.Type == 'AMAZON_ISSUED':
            self.logger.info(
                "Cert %s had cert tran logging disable successfully", self.url)

    def enable_transparency_logging(self):
        """Classmethod to enable certificate transparency logging on
        this certificate"""
        if self.Issuer == 'Amazon' and self.Type == 'AMAZON_ISSUED':
            self.logger.info(
                "Cert %s had cert tran logging enabled successfully", self.url)

    def __repr__(self):
        return str(self.__dict__)
