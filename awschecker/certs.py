
import logging
import boto3
import constants
from .classes import AWSCertificate
from .decorator_logging import logged


@logged(logging.DEBUG)
def check_items():
    """Queries AWS regions for ACM certificates, and then checks them."""

    logger = logging.getLogger(__name__)
    logger.debug("Begin searching for certificates.")

    for region in constants.PREFERRED_REGIONS:
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
    logger.debug("End searching for certificates.")


@logged(logging.DEBUG)
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
