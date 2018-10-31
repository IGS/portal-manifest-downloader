# DCPPC Portal Manifest Downloader

The DCPPC Portal Manifest Downloader must be be run on a cloud-based virtual machine (VM) to remain compliant with NIH Data Commons Pilot Phase Consortium (DCPPC) data access policies. Only users that have been onboarded and received approval for access to controlled data may access resources via the DCPPC Portal. Users must have read and agreed to the NIH data access policy at https://gdc.cancer.gov/access-data/data-access-policies, as well as agreed to abide by the NIH Code of Conduct for Genomic Data Use at: https://dbgap.ncbi.nlm.nih.gov/aa/GWAS_Code_of_Conduct.html

To start the onboarding process to gain access, please begin [here](https://hackmd.io/s/rkhHC2cFf).

## Dependencies

On your cloud-based VM, ensure that you have git installed as well as Python 3.x.

The downloader requires Python 3 as well as the 'requests' and 'oauth2client' libraries:

[Python 3](https://www.python.org/downloads/)

[requests](https://pypi.org/project/requests/)

[oauth2client](https://pypi.org/project/oauth2client/)

One easy way to install Python 3 and the necessary dependencies is to use [Virtualenv](https://virtualenv.pypa.io).

## Executing the downloader

1) On your cloud-based VM, download this utility:
```
$ git clone https://github.com/dcppc-phosphorous/manifest-downloader.git
```

2) Run the downloader:
```
$ ./bin/get_dcppc_manifest.py -m <manifest_id>
```

You will be presented with a URL which will authenticate you so that you may obtain an access token. This token will be pasted back into the program's input so that the manifest may be downloaded.
