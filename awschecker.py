"""
awschecker.pyc
Inspects an AWS account for ACM certificates.
Reports on invalid certificates, pending certificates, and certificates with
certificate transparency enabled.
"""

import logging
import logging.config
from os import path
from awschecker import ec2instances
from awschecker import certs
from awschecker.decorator_logging import logged
import constants


def log_path():
    """Gets the OS and environment independent path to the logger configuration file."""
    log_file_path = path.join(path.dirname(path.abspath(__file__)), constants.LOGCONFIG)
    return log_file_path

logging.config.fileConfig(log_path())
LOGGER = logging.getLogger(__name__)

@logged(logging.DEBUG)
def main():
    """Applicationentry point."""

    ec2instances.check_items()
    certs.check_items()

    logging.shutdown()


if __name__ == "__main__":
    main()
