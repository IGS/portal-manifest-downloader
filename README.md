# DCPPC Portal Manifest Downloader

The DCPPC Portal Manifest Downloader is meant to be run on a cloud-based VM to remain compliant with the NIH data access policy: https://gdc.cancer.gov/access-data/data-access-policies

## Dependencies

On your cloud-based VM, ensure that you have git installed as well as Python 3.x. The Python modules 

The downloader requires Python 3 and the requests library:

[Python 3](https://www.python.org/downloads/)

[requests](https://pypi.org/project/requests/)

One easy way to install Python 3 and the necessary dependencies is to use [Virtualenv](https://virtualenv.pypa.io).

## Running the downloader

1) On your cloud-based VM, download this utility:
```
$ git clone https://github.com/dcppc-phosphorous/manifest-downloader.git
```

2) Run the downloader:
```
$ ./bin/get_dcppc_manifest.py -m <manifest_id> -u <username>
```

You will be asked for your DCPPC Portal password as well.

