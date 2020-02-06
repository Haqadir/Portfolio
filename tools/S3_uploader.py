#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

###############################################################################
# Copyright (C) 2014+ MyWorld, Inc. All rights reserved.                      #
#                                                                             #
# The information and source code contained herein is the exclusive property  #
# of MyWorld, Inc. No part of this software may be used, reproduced, stored   #
# or distributed in any form, without explicit written authorization from     #
# MyWorld, Inc.                                                               #
###############################################################################

'''Send file to box folder

Requires 'credentials.py' file containing:
  _BOX_USER := box username
  _BOX_PSWD := box password
'''

# Standard library imports
import ftplib
import os.path
import argparse
import datetime
import sys
import subprocess


###############################################################################

tree = {
    # POC - TBD URLs
    'int_cls':         { 'node':'s3://e3-snowflake/stage/loblaw/Manual_loads/internal_cleanse/', 'URL': 'https://s3.console.aws.amazon.com/s3/buckets/e3-snowflake/stage/loblaw/Manual_loads/internal_cleanse/?region=us-west-1&tab=overview' },
    'e3_instore':      { 'node':'s3://e3-snowflake/stage/loblaw/Manual_loads/E3_Instore/', 'URL':  'https://s3.console.aws.amazon.com/s3/buckets/e3-snowflake/stage/loblaw/Manual_loads/E3_Instore/?region=us-west-1&tab=overview'},
    'None':			   { 'node':'', 'URL':  ''}
}

def send_to_aws(filename, directory_path):
    subprocess.call( 'aws s3 cp {0} {1}'.format(filename, directory_path), shell=True)

    

###############################################################################

if __name__ == '__main__':
    print('-'*80)

    restricted_values = []
    for key, value in tree.items():
        restricted_values.append(key)

    parser = argparse.ArgumentParser()
    parser.add_argument('-file', required=False, nargs='+', help='full path to file locally')
    parser.add_argument('-path', required=False,  help='Destination in BOX\n\tPossible values: {0}'.format(restricted_values.sort()))
    
    args =  parser.parse_args()
    print('')
    

    

    if args.path is None:
        print('Stored locations where you can upload file to S3:\n')
        for key,value in tree.items():
            print(key)
        path=input('chose a path alias: ')

    if args.file is None:
        file = input('What file do you want to send? ')

    assert path in restricted_valuess
    # auto fill in dynamic path for billing
    path = tree[args.path]['node']
    URL = tree[args.path]['URL']

    send_to_aws(args.file , path)

    print(' see URL: {0}'.format(URL))
    print('-'*80)
