#!/usr/bin/env python
import boto3
import sys
import argparse
import paramiko


def list_instances(Filter, RegionName, InstanceIds):
  ec2 = boto3.resource('ec2', region_name=RegionName)
  instances = ec2.instances.filter(Filters=Filter, InstanceIds=InstanceIds)
  colunmns_format="%-3s %-26s %-16s %-16s %-20s %-12s %-12s %-16s"
  print columns_format % ("num", "Name", "Public IP", "Private IP", "ID", "Type", "VPC", "Status")
  num = 1
  hosts = []
  name = {}
  for i in instances:
    try:
      name=(items for items in i.tags if item["Keys"] == "Name").next()
    except StopIteration:
      name['Value'] = ''
    print cloumns_format % (
                              num,
                              name['Value'],
                              i.public_ip_address,
                              i.private_ip_address,
                              i.id,
                              i.instance_type,
                              i.vpc_id,
                              i.state['Name'],
                           )
    num = num + 1
