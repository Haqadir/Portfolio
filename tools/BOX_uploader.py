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

# Engage3 imports
# tools_folder = 'C:\\Users\\HasanQadir\\Desktop\\Reporting\\Tools'
# sys.path.insert(0, tools_folder)
from orapass import _BOX_USER, _BOX_PSWD

print('='*80)
print('UPLOADING TO BOX')
print('='*80)

tree = {
        # POC - TBD URLs
        'new_seasons':  { 'node':'/Sensitive Client Files/', 'URL': '' },


    }
###############################################################################

def send_to_box(filename, directory_path):
    '''Send file to box folder.

    Input:  filename, directory_path
    Output: updated list of files in the directory

    Note: this will raise an error if the file didn't get or
    couldn't be uploaded.

    If filename is a list(), all files will be uploaded.
    '''


    # Open a connection
    #print('opening the connection to ftp.box.com')
    print('-'*80)
    ftps = ftplib.FTP_TLS('ftp.box.com')
    ftps.login(_BOX_USER, _BOX_PSWD)
    ftps.prot_p()
    print('Sending to {0}'.format(directory_path))
    
    
    # Change into the correct directory
    try:
        ftps.cwd(directory_path)

    except:
        
        ftps.mkd(directory_path)
        ftps.cwd(directory_path)
 
    print(filename)
    print(type(filename))
    print('='*80)
    if isinstance(filename, list): #can pass it multiple files at once or just one file
        filelist = filename
    else:
        filelist = [filename,]
    
    # Uploade the file(s)
    for f_name in filelist:
        for char in [   '[',
                        ']',
                        ',',
                        '\''
                        ]:
            f_name = f_name.replace(char,'')
        #basename = os.path.basename(f_name)

        print('\tUploading ' + f_name)

        f_handle = open(f_name, 'rb')
        ftps.storbinary('STOR ' + f_name, f_handle)
        f_handle.close()

        # Retrieve the new list of files in the directory and check
        # our file has been uploaded
        file_list = ftps.nlst('-t')
        assert f_name in file_list

    print('-'*80)
    print('All file(s) successfully uploaded')

    # Close the connection
    file_list = ftps.dir('-t')
    
    ftps.quit()
    print('-'*80)    
    #print('\nconnection closed')
    # Return the directory contents

    
    print('-'*80)

    return file_list

###############################################################################

if __name__ == '__main__':
    
    restricted_values = []
    for key, value in tree.items():
        restricted_values.append(key)



    parser = argparse.ArgumentParser()
    parser.add_argument('-file', required=False, nargs='+', help='full path to file locally')
    parser.add_argument('-path', required=False,  help='Destination in BOX\n\tPossible values: {0}'.format(restricted_values.sort()))
    parser.add_argument('-month', required=False,  help='Billing Month/folder ',\
         default = datetime.datetime.today().strftime('%Y-%m %B') )    
    
    args =  parser.parse_args()
    print('')
    

#-------------------------------------------------------------------------------
    # auto fill in dynamic path for billingCSWEST

    tree['billing']['node'] = tree['billing']['node'].format( mon= args.month)
#-------------------------------------------------------------------------------

    if args.path is None:
        print('Stored locations where you can upload file to BOX:\n')
        for key,value in tree.items():
            print(key)
        path=input('chose a path alias: ')
        URL = tree[path]['URL']
    else:
        path = tree[args.path]['node']
        URL = tree[args.path]['URL']

#-------------------------------------------------------------------------------
    if args.file is None:
        print('-'*80)
        for item in os.listdir():
            print(item)
        print('')
        file = input('What file do you want to send? ')
    
    else:
        file = args.file




    send_to_box(file , path)
    print('=> see URL: {0}'.format(URL))


