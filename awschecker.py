
from boto3.session import Session
import sqlite3
from sqlalchemy import create_engine
import logging, logging.config


from awschecker import certs

db = create_engine('sqlite:///:memory:', echo=True)


def main():
    logging.config.fileConfig('logging_config.ini')
    logger = logging.getLogger(__name__)


    logger.debug ("Begin processing.")
    certs.check_certs()
    logger.debug("End processing")


if __name__ == "__main__":main()
