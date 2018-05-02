
#!/usr/bin/env python

# Copyright 2017, Keith Sharp, <kms@passback.co.uk>
# Released under the Apache Licence 2.0: https://www.apache.org/licenses/LICENSE-2.0 

# Small script to parse an AWS ARN and get it's separate components:
#
#   arn
#   partition (normally aws)
#   service
#   region
#   account-id
#   resource or resourcetype/resource or resourcetype:resource
#
# https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html

from __future__ import print_function
import logging


def error_exit(message):
    logger = logging.getLogger(__name__)
    logger.error(message)
    print(message, file=sys.stderr)


class AWSARN(object):
    """Takes an AWS ARN and splits it into it's components"""

    def __init__(self, arn):
        self.arn = arn
        self.__parse()

    def __str__(self):
        return self.arn

    def __parse(self):
        list = self.arn.split(':')
        if len(list) < 6 or len(list) > 7:
            error_exit("Wrong number of components: " + self.arn)
        if list[0] != 'arn':
            error_exit("ARN must start with 'arn': " + self.arn)

        self.partition = list[1]
        self.service = list[2]
        self.region = list[3]
        self.account = list[4]

        if len(list) == 6:
            reslist = list[5].split('/')
            if len(reslist) == 1:
                self.resourcetype = ""
                self.resource = list[5]
            else:
                self.resourcetype = reslist[0]
                self.resource = '/'.join(reslist[1:])

        if len(list) == 7:
            self.resourcetype = list[5]
            self.resource = list[6]

    @property
    def arn(self):
        return self.__arn

    @arn.setter
    def arn(self, arn):
        self.__arn = arn

    @property
    def partition(self):
        return self.__partition

    @partition.setter
    def partition(self, partition):
        self.__partition = partition

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, service):
        self.__service = service

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, region):
        self.__region = region

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account):
        self.__account = account

    @property
    def resourcetype(self):
        return self.__resourcetype

    @resourcetype.setter
    def resourcetype(self, resourcetype):
        self.__resourcetype = resourcetype

    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, resource):
        self.__resource = resource

    
    def __repr__(self):
        return str(self.__dict__)