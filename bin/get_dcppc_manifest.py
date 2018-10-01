#!/usr/bin/env python

import argparse
import sys
import requests
import getpass

"""DCPPC manifest Downloader

Source: https://github.com/dcppc-phosphorous/manifest-downloader

This software is used in conjunction with the portal.nihdatacommons.us site
to allow DCPPC users to download the manifests which have been saved to the
cloud during use of that website.

Example:

        $ python -m <manifest-id> -u <username> get_dcppc_manifest.py

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

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--manifest-id", help="ID that was presented when the Manifest file was sent to S3")
parser.add_argument("-u", "--username", help="Your username for accessing https://portal.nihdatacommons.us/")
args = parser.parse_args()

if not (args.manifest_id and args.username):
    print("Must supply id and username")
    parser.print_help(sys.stderr)
    sys.exit(1)

prompt="Do you agree that you are executing this in a cloud environment per the policies of the DCPPC and also that you have read and agree to the NIH data access policy (https://gdc.cancer.gov/access-data/data-access-policies)?"

confirmation = query_yes_no(prompt)

print ("\nPlease enter your DCPPC Password")
pw = getpass.getpass()

filename = 'dcppc_manifest_' + args.manifest_id + '.tsv'
url = 'http://portal.nihdatacommons.us/api/manifest?id=' + filename
print ("Fetching manifest...")

response = requests.get(url, auth=requests.auth.HTTPBasicAuth(args.username, pw))

if response.status_code == 404 or response.status_code == 500:
    filename = 'dcppc_manifest_metadata_' + args.manifest_id + '.tsv'
    url = 'http://portal.nihdatacommons.us/api/manifest?id=' + filename
    response = requests.get(url, auth=requests.auth.HTTPBasicAuth(args.username, pw))

if response.status_code != 200:
    if response.status_code == 404:
        print("No manifest was found with the given ID")
    else:
        print("An HTTP response code of " + str(response.status_code) + " was returned")
        print(response.content)
else:
    with open(filename, 'wb') as f:
        f.write(response.content)
    print ("Done.")

