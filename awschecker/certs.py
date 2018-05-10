
import boto3
#from awschecker.classes import certificate
from boto3.session import Session
import logging
from .classes import AWSCertificate
from .classes import AWSARN


def check_items():
    """Queries AWS regions for ACM certificates, and then checks them."""

    logger = logging.getLogger(__name__)
    logger.info("Begin searching for certificates.")
    s = Session()
    
    for region in s.get_available_regions('acm'):
        logger.debug("Searching region: %s", region)
        client = boto3.client('acm', region_name=region)
        response = client.list_certificates()

        for cert in response.get("CertificateSummaryList"):
            logger.debug("The cert header: %s", cert)

            description = client.describe_certificate(
                CertificateArn=cert['CertificateArn'])

            mycert = AWSCertificate(description=description['Certificate'])
            logger.debug(mycert)
            check_one_item(mycert)
    logger.info("End searching for certificates.")


def check_one_item(mycert):
    """Takes a certificate object, and performs validation checks."""

    logger = logging.getLogger(__name__)

    if mycert.Status.upper() != 'ISSUED':
        logger.warn("Cert %s is not issued (%s).",
                    mycert.url, mycert.Status)
    elif mycert.CertificateTransparencyLoggingPreference.lower() == 'enabled':
        logger.warn(
            "Cert %s certificate transparency logging is enabled.", mycert.url)
        # mycert.disable_transparency_logging()
    else:
        logger.info(
            "Cert %s certificate transparency logging is disabled.", mycert.url)
        # mycert.enable_transparency_logging()
