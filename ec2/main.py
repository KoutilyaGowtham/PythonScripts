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
  
  session=boto3.Session(profile_name=args.aws_profile)
  ec2=session.resource('ec2')
  client=session.client('ec2')
  
  #KeyPair
  
  if args.aws_key:
    key_name=args.aws_key
  
  if args.aws_type:
    key_name=args.aws_type
    
  try:
    key_pair=ec2.keypair(key_name)
    key_pair.load()
    logger.info("Found keypair with fingerprint")
    logger.info(key_pair.key_fingerprint)
    
  except:
    try:
      r = client.create_key_pair(KeyName=key_name)
      print("Key is Created")
      
      with open(key_name + '.pem', w) as f:
        f.write(r['keyMaterial'])
        print("Downloaded Keypair")
        
        key_pair=ec2.keypair(key_name)
        key_pair.load()
        logger.info("Found keypair with fingerprint")
        logger.info(key_pair.key_fingerprint)
      
    except Exception as e:
      print(e)
      logger.error("Unable to create key.")
    
    ## Creating Instance
    
    r = client.describe_instances(Filters=[{'Name':'key-name','Values':[key_name]}])
    if len(r['Reservations']) > 0:
      for res in r['Reservations']:
        for ins in res['Instances']:
          ins_id=ins['InstanceId']
          ins_state=ins['State']['Name']
          if not args.info:
            print('Instance %s is %s' % (ins_id,ins_state))
          if ins_state not in('shutting-down', 'terminated'):
            instance_id = ins_id
            instance_state = ins_state
            if args.info:
              if args.verbose:
                print('Image Id: %s' % ins['ImageId'])
                print('Instance Id: %s' % ins['InstanceId'])
                print('Instance type: %s' % ins['InstanceType'])
                print('Public Ip: %s' % ins['PublicIpAddress'])
                print('Public DNS Name: %s' % ins['PublicDNSName'])
                
              else:
                print(ins['PublicDNSName'])
                
    if instance_id == None:
      if args.remove:
        print('No instance found')
        sys.exit(0)
      else: 
        if args.info:
          sys.exit(0)
        try:
          logger.info('Creating a new instance')
          r = cient.run_instances(
            Image_Id=aws_image,
            Min_count=1,
            Max_count=1,
            KeyName=key_name,
            InstanceType=instance_type,
            InstanceInitiatedShutdownBehaviour='terminate',
          )
          instance_id = r['Instances'][0]['InstanceId']
          instance_state = r['instances'][0]['State']['Name']
          print('Instance %s is %s' % (instance_id,instance_state))
        except:
          print('Unable to create Instance')
        
           
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
            
      
