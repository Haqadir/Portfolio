#Standardized directory set up for reporting 
import os
import sys
import subprocess

reporting_dir = '/Users/hqadir/OneDrive\ -\ My\ World\,\ Inc/Desktop/Reporting/'

clientdir=input('enter client folder name to be added to reporting directory: ')
new_dirname = reporting_dir+clientdir

print('-'*80)
print('setting up standard folders...')
print('-'*80)

subprocess.call( 'mkdir {0}'.format(new_dirname) , shell=True)
subprocess.call( 'mkdir {0}/client_files'.format(new_dirname) , shell=True)
subprocess.call( 'mkdir {0}/crawl_archive'.format(new_dirname) , shell=True)
subprocess.call( 'mkdir {0}/delivery_archive'.format(new_dirname) , shell=True)
subprocess.call( 'mkdir {0}/scripts'.format(new_dirname) , shell=True)


print('\nSet Up Complete.')
print('-'*80)