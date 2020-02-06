
# Standard library imports
import paramiko
import sys
import os.path
import argparse
import datetime
import pandas as pd
import os
from sqlalchemy import create_engine
import subprocess

# Engage3 imports
from orapass import _sf_prod, ftp_accts
# FTP Credentials

root = os.path.dirname(os.getcwd())

###############################################################################

def get_from_ftp_sflogging( url,directory_path, account,logging_table = 'DB.SCHEMA.TABLE', test=0):
    print('Accessing account : {0}'.format(account))
    #Client folders
    if account == 'LCL':
        tree = {
            'int_cls': '/Internals',  
            'volume' : "/volume history"

        }

    if account == 'LCLB':
        tree =  {
            'int_cls':   "/Internals",
            'volume': "/Volumes"
        }

    if account == 'LCLB2':
        tree =  {
            'volume':   "/Volume History",
            'int_cls': '/history',

        }


    # Open a connection
    print('opening the connection to {0}'.format(url))
    ssh_c = paramiko.SSHClient()
    ssh_c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_c.connect(hostname=url,username= ftp_accts[account]['usr'], password= ftp_accts[account]['pass'])

    ftps = ssh_c.open_sftp()
    print('connection opened')



    # Uncomment below during testing
    #processed = processed[:-1]


    # Change into the correct directory
    try:
        a = tree[directory_path]
        print(a)
        ftps.chdir(a)
        file_list = ftps.listdir()
    except:
        print('unable to locate target directories')
        file_list=[]
#---------------------------------------------------------
    #   get list of items currently in FTP by time uploaded




    #----------------------------------------------------------
    #check log to see what files are new that should be downloaded
    print('accessing log from Snowflake')
    engine = create_engine(_sf_prod)
    log=pd.read_sql('select * from {0} order by processed_time desc limit 100'.format(logging_table),engine) # File | Timestamp_processed  
    print('-'*80)
    print(log)
    print('-'*80)
    processed = [x.lower() for x in log.sort_values(by=['processed_time'], ascending=False )['file'].unique()]
    print()
#---------------------------------------------------------------
    new_file_list=[]
    if len(file_list)==0:
        pass
    else:
        
        for entry in file_list:
            f_name = entry.lower()
            if (f_name not in processed) & (f_name not in os.listdir()):
                new_file_list.append(f_name)
                print('\t| NEW FILE FOUND: retrieving ' + f_name)

                if int(test) == 0:
                    ftps.get(f_name ,  f_name )
                    #ftps.get(f_name , os.getcwd() + '\\' + f_name )

                    print('\t| Recording to Logging table')
                    # Do this.
                    print('establishing connection')
                    connection = engine.connect()
                    try:
                        print('insert statement')
                        connection.execute('insert into {0} values ( \'{1}\', current_timestamp() ) '.format(logging_table,f_name.lower()))
                    finally:
                        connection.close()
                        engine.dispose()
                else:
                    print('Testing mode - skipped:\n\t- Downloading of file\n\t- Recording to Log table ')
            else:
                continue


    if len(new_file_list)>0:
        print('\t| All file(s) successfully Downloaded')
        #status = 1 # meaning, yes proceed to downstream program - we are sending a file to work with
    else:
        print('\t| No new files...')
        #status = 0




    # Close the connection
    ftps.close()
    print('\t| connection closed\n')
        # Return the directory contents
    
    # except:
    #     print('Directory has no files or directory doesn\'t exist')
    #     new_file_list = None

    return new_file_list



###############################################################################




if __name__ == '__main__':


    restricted_values = []
    for key, value in tree.items():
        restricted_values.append(key)

    parser = argparse.ArgumentParser()
    parser.add_argument('-url',required=True,help='host url')
    parser.add_argument('-path', required=False,  help='Destination in BOX\n\tPossible values: {0}'.format(restricted_values))
    parser.add_argument('-logfile', default = 'DB.SCHEMA.TABLE')
    parser.add_argument('-acct', required = True)
    #parser.add_argument('-ftype', required=False, help='file type or pattern, e.g. \'.csv\' or \'_CS.csv\' ')

    args =  parser.parse_args()
    print('')


#-------------------------------------------------------------------------------

   
    
    get_from_ftp_sflogging( url= args.url, directory_path = args.path, account=args.acct,logging_table = 'DB.TABLE.SCHEMA')
