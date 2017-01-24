#!/usr/bin/env python

import httplib2 as http
import json
import argparse
import ConfigParser
import sys
import os 
import stat

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

vspath = '/mgmt/tm/ltm/virtual'

configfile = 'f5status.conf'

config = ConfigParser.ConfigParser()
config.read(configfile)

parser = argparse.ArgumentParser(description='Fetch LB environment statuses')
parser.add_argument('--node', '-n', default=None, required=True, help='Node to query via the REST API')
parser.add_argument('--env', '-e', default=None, required=True, help='Customer e.g. LAB, PROD, TEST etc.')
parser.add_argument('--user', '-u', default="admin", required=True, help='The username of the API user')
parser.add_argument('--password-from-file', '-pff', default=None, required=True, help='Path to API user password file')
args = parser.parse_args()

passwordfile = args.password_from_file

try:
    st = os.stat(passwordfile)
except OSError as e:
    print 'OSError: ' + str(e)
    sys.exit(1)

if not st.st_mode == 33024:
    print 'Error! The permissions on ' + passwordfile + ' should be 400 (only readable by owner) not ' + oct(st.st_mode)[4:] + '. Please chmod as needed.'
    sys.exit(1)
else:
    pfh = open(passwordfile, 'r')
    password = pfh.readline().strip()

username = args.user

try:
    apiendpoint = config.get(args.env, args.node)
except ConfigParser.NoSectionError as e:
    print e.message
    sys.exit(1)
except ConfigParser.NoOptionError as e:
    print e.message
    sys.exit(1)

def fetchData(url, username, password, apipath=''):

        method = 'GET'
        body = ''
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close'
            }

        h = http.Http(disable_ssl_certificate_validation=True)
        h.add_credentials(username, password)

        apiurl = urlparse(url + apipath)

        response, content = h.request(
                apiurl.geturl(),
                method,
                body,
                headers)
        
        statuscode = response.status
        reason = response.reason

        if statuscode != 200:
            print 'Response ' + str(statuscode) + ' - ' + reason
            sys.exit(1)
        else:
            data = json.loads(content)
            return data
        
def fetchStatus(url, username, password):
    statusdata = fetchData(url, username, password, '')
    
    return statusdata
    
def cleanUrl(url):
    if 'localhost' in url:
        url = url.replace('https://localhost', apiendpoint)
        url = url.replace('?ver=11.6.0', '')

    return url

apidata = fetchData(apiendpoint, username, password, vspath)

count = 0

print '{0:45} {1:45} {2}'.format('VS', 'Destination', 'Status')
print '-' * 98

for vs in apidata['items']:
    count = count + 1
    vsstats = fetchStatus(cleanUrl(vs['selfLink']) + '/stats', username, password)
    status = {}

    for k,v in vsstats['entries'].iteritems():
        status['name'] = vs['name']
        status['destination'] = vs['destination']
        if 'status' in k:
            status[k] = v['description']
    
    if status['status.availabilityState'] == 'offline' and status['status.enabledState'] == 'disabled':
        color = '\033[0;37;40m' # black
    elif status['status.availabilityState'] == 'available':
        color = '\033[0;37;42m' # green 
    elif status['status.availabilityState'] == 'unknown':
        color = '\033[0;37;44m' # blue
    elif status['status.availabilityState'] == 'offline':
        color = '\033[0;37;41m' # red 
    else:
        color = '\033[0m' # normal
    
    statusstr = status['status.availabilityState'] + ' (' + status['status.enabledState'] + ') - ' + status['status.statusReason']

    print color + '{0:45} {1:45} {2}\033[0m'.format(status['name'], status['destination'], statusstr)

