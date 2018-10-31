#!/usr/bin/env python

import argparse
import requests
import json
import tempfile
import sys
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

"""DCPPC manifest Downloader

Source: https://github.com/dcppc-phosphorous/manifest-downloader

This software is used in conjunction with the portal.nihdatacommons.us site
to allow DCPPC users to download the manifests which have been saved to the
cloud during use of that website.

Example:

        $ python get_dcppc_manifest.py -m <manifest-id> 

Note: The manifest-id is issued by the portal.nihdatacommons.us site and
presented to the user at the time the manifest file is saved to the cloud.

"""

def query_yes_no(question, default="no"):
    """Ask a yes/no question via input() and return user's answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

MANIFEST_URL = "http://portal-staging.nihdatacommons.us/api/manifest/download?id="


myparser = argparse.ArgumentParser(description="Obtain the portal manifest by ID.")
myparser.add_argument('-m', '--manifest',
                    required=True,
                    help="Specify the manifest ID issued by the Portal.")
myparser.add_argument('--logging_level', default='ERROR',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      help='Set the logging level of detail.')

# Parse the arguments from the CLI
args = myparser.parse_args()

prompt="\nDo you agree that you are executing this in a cloud environment per the policies \n" + \
       "of the DCPPC and also that you have read and agree to the NIH data access policy \n" + \
       "at https://gdc.cancer.gov/access-data/data-access-policies?"

confirmation = query_yes_no(prompt)
if not confirmation:
    sys.exit(0)

# Generate a temporary file. A file is required when instantiating
# a Storage object, which we need to later invoke oauth's run_flow()
temp_file = tempfile.NamedTemporaryFile(delete=True).name
storage = Storage(temp_file)

# Setup the scope of what to access...
SCOPE = 'https://www.googleapis.com/auth/userinfo.profile'

flow = flow_from_clientsecrets('client_id.json', scope=SCOPE)

# Force the assumption that there is a headless environment and 
# that a graphical browser and local webserver are NOT available.
args.noauth_local_webserver=True

# Get the manifest ID from what the user specified on the CLI.
manifest_id = args.manifest

# Now we create our Credentials object (for which we needed the temporary
# file and command line arguments).
credentials = tools.run_flow(flow, storage, args)

# Grab the necessary tokens
token_response = credentials.token_response
access_token = token_response['access_token']
id_token = token_response['id_token']

headers = {'Authorization': 'Bearer {}'.format(access_token)}

print("---------------------------------------------")

# Assume a regular manifest file using the given ID.

filename = 'dcppc_manifest_' + manifest_id + '.tsv'
print ("Fetching manifest...")
response = requests.get(MANIFEST_URL + filename, headers=headers)

# if no file returned, try a manifest metadata file with the given ID
if response.status_code == 404 or response.status_code == 500:
    filename = 'dcppc_manifest_metadata_' + manifest_id + '.tsv'
    response = requests.get(MANIFEST_URL + filename, headers=headers)

if response.status_code != 200:
    if response.status_code == 404:
        print("No manifest was found with the given ID")
    else:
        print("HTTP error " + str(response.status_code) + " was retuned")
        print(response.content)
else:
    with open(filename, 'wb') as f:
        f.write(response.content)
        print("Manifest saved to {}.".format(filename))
