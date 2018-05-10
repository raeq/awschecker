
from boto3.session import Session
import sqlite3
from sqlalchemy import create_engine
import logging, logging.config
from os import path
from awschecker import certs

LOGCONFIG = 'logging_config.ini'

def log_path():
    log_file_path = path.join(path.dirname(path.abspath(__file__)), LOGCONFIG)
    return log_file_path

def main():
    logging.config.fileConfig(log_path())
    logger = logging.getLogger(__name__)


    certs.check_certs()


if __name__ == "__main__":main()


