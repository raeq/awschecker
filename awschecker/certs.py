
import boto3
#from awschecker.classes import certificate
from boto3.session import Session
import logging
from .classes import AWSCertificate
from .classes import AWSARN


def check_certs():

    logger = logging.getLogger(__name__)
    logger.info("Begin searching for certificates.")
    s = Session()
    acm_regions = s.get_available_regions('acm')

    for region in acm_regions:
        logger.debug("Searching region: %s", region)
        acmclient = boto3.client('acm', region_name=region)
        response = acmclient.list_certificates()

        for cert in response.get("CertificateSummaryList"):
            logger.debug("The cert header: %s", cert)

            description = acmclient.describe_certificate(
                CertificateArn=cert['CertificateArn'])

            mycert = AWSCertificate(description['Certificate'])
            logger.debug(mycert)
            check_one_cert(mycert)
    logger.info("End searching for certificates.")



def check_one_cert(mycert):
    logger = logging.getLogger(__name__)

    if mycert.Status != "ISSUED":
        logger.warn("Cert %s is not issued (%s).",
                    mycert.ARN.arn, mycert.Status)
    elif mycert.CertificateTransparencyLoggingPreference != "Enabled":
        logger.warn(
            "On cert %s certificate transparency logging is enabled.", mycert.url)
    else:
        logger.warn(
            "On cert %s certificate transparency logging is disabled.", mycert.url)
