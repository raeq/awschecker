"""
awschecker.pyc
Inspects an AWS account for ACM certificates.
Reports on invalid certificates, pending certificates, and certificates with 
certificate transparency enabled.
"""


from boto3.session import Session
import sqlite3
from sqlalchemy import create_engine
import logging
import logging.config
from os import path
from awschecker import ec2instances
from awschecker import certs
from awschecker.decorator_logging import logged


def log_path():
    """Gets the OS and environment independent path to the logger configuration file."""
    log_file_path = path.join(path.dirname(path.abspath(__file__)), LOGCONFIG)
    return log_file_path

LOGCONFIG = 'logging_config.ini'
logging.config.fileConfig(log_path())
logger = logging.getLogger(__name__)    

@logged(logging.DEBUG)
def main():
    """Applicationentry point."""
    logger = logging.getLogger(__name__)    

    ec2instances.check_items()
    certs.check_items()

    logging.shutdown()


if __name__ == "__main__":
    main()
