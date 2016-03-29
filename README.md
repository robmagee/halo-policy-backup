# halo-policy-backup [![Build Status](https://travis-ci.org/robmagee/halo-policy-backup.svg?branch=master)](https://travis-ci.org/robmagee/halo-policy-backup)[![Coverage Status](https://coveralls.io/repos/github/robmagee/halo-policy-backup/badge.svg?branch=master)](https://coveralls.io/github/robmagee/halo-policy-backup?branch=master)

The script is to backup policies from each module in Halo. It is strongly recommended that you backup your policy before/after making any changes.

## Notes
The Halo API only supports more modern versions of OpenSSL.  Many python distributions on OSX and Windows contain python executables
that were built against older, less secure versions of OpenSSL.  If you are having problems connecting using your python distribution
you will need to upgrade your system's OpenSSL.  For notes on how to do this on OSX with Python 3.5 or 2.7 see the notes in the
*PYTHON_OPENSSL* file.


# Steps
***1.*** Download/Clone this repository to your local machine

***2.*** Edit config.conf

***3.*** Run `python halo-policy-backup.py`

# Requirements and Dependencies

To get started, you must have the following privileges and software resources:

* An active CloudPassage Halo subscription. If you don't have one, Register for CloudPassage to receive your credentials and further instructions by email.
* Access to your CloudPassage API key. Create a new key, with write privileges, specifically for use with this script.
* Python 2.6 or later.
* If you don't have gitpython installed, please install it via your terminal.
```
pip install gitpython
```
* The Python 2 and 3 Compatibility Library is also required.  If you do not have it,
please install via the following command:
```
pip install six
```

<!---
#CPTAGS:community-supported archive
#TBICON:images/python_icon.png
-->
