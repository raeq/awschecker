
import boto3
#from awschecker.classes import certificate
from boto3.session import Session
import logging
from .classes import AWSCertificate
from .classes import AWSARN



def find_certs():

    logger = logging.getLogger(__name__)
    logger.debug("Begin searching for certificates.")
    all_certs = {}
    s = Session()
    acm_regions = s.get_available_regions('acm')

    for region in acm_regions:
        logger.debug("Searching region: %s",region)
        acmclient = boto3.client('acm', region_name=region)
        response = acmclient.list_certificates()

        for cert in response.get("CertificateSummaryList"):
            logger.debug("The cert header: %s",cert)

            description = acmclient.describe_certificate(
                CertificateArn=cert['CertificateArn'])

            mycert = AWSCertificate(description['Certificate']['CertificateArn'],
                                    description['Certificate']['DomainName'],
                                    description['Certificate']['Status'],
                                    description['Certificate']['Options']['CertificateTransparencyLoggingPreference'],
                                    description['Certificate']['Serial']
                                    )
            logger.info(mycert)
            all_certs[mycert.ARN]=mycert

    logger.debug(all_certs)
    return all_certs

def check_certs():
    logger = logging.getLogger(__name__)
    all_arns=find_certs()
    for arn in all_arns:
        mycert = all_arns[arn]
        if mycert.Status != "ISSUED":
            logger.warn("Cert %s is not valid.", arn)
        if mycert.CertificateTransparencyLoggingPreference != "Enabled":
            logger.warn("On cert %s certificate transparency logging is enabled.", arn)
