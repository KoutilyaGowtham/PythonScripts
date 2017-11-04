#!/usr/bin/env python
import boto3
import sys
import argparse
import paramiko


def list_instances(Filter, RegionName, InstanceIds):
