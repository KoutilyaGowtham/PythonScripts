#!/usr/bin/env python

import sys
import os
import json
import argparse
from pprint  import pprint
import boto3
from utils import logger

#########################################################

key_name = "windowsnew"
aws_image = "ami-c998b6b2"
instance_type = "t2.micro"

Parser = argparse.ArgumentParser(description='Simple CLI / module to create/start/stop EC2 instances')
parser.add_argument('-p', '--profile', dest='aws_profile', metavar="AWS_PROFILE", help="AWS Profile Name")
parser.add_argument('-k', '--key', dest='aws_key', metavar="AWS_KEY", help="AWS Key name to use. Default: %s" % key_name)
parser.add_argument('-t', '--type', dest='aws_type', metavar="AWS_INS_TYPE", help="AWS Instance type. Default: %s" % instance_type)
parser.add_argument('-d', '--dry-run', action='store_true', help="Dry run")
parser.add_argument('-i', '--info', action='store_true', help="Print instance info. Default: Only IP to allow usage in other scripts. If verbose is set, prints additional info.")
parser.add_argument('-s', '--stop', action='store_true', help="Stop the instance")
parser.add_argument('-r', '--remove', action='store_true', help="Remove: Terminate instance and delete created key")
parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")

args = parser.parse_args()

#################################################################

def main():
  global key_name,aws_image,instance_type
  
  session = None
  ec2 = None
  client = None
  key_pair = None
  instance_id = None
  instance_state = None

