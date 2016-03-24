import os
import sys
from os import path
from six.moves import configparser

# Returns boolean for path sanity.


def check_path(basepath):
    sane = True
    basepath = basepath or "."
    paths = [path.join(basepath, x)
             for x in ("fim",
                       "csm",
                       "firewall",
                       "lids")]
    for p in paths:
        if os.path.isdir(p) == False or os.access(p, os.W_OK) == False:
            print("Path {0} does not exist or rights are insufficient. "
                  "Creating the directory with proper permissions.".format(p))
            try:
                curmask = os.umask(0)
                os.makedirs(p, 0o770)
            except os.error as oe:
                print(oe.strerror)
                sane = False
            finally:
                os.umask(curmask)
    return sane

# Check sanity of config file


def check_config(config):
    sane = True
    apihost = ["api.cloudpassage.com",
               "api.lichi.cloudpassage.com",
               "api.bass.cloudpassage.com",
               "api.zink.cloudpassage.com"]
    try:
        # make sure all the values are there and the lenghts match
        if not config.get("halo", "api_host") in apihost or \
            len(config.get('halo', 'api_key')) != 8 or\
            len(config.get('halo', 'api_secret')) != 32:
            raise configparser.Error('Ensure you have an 8 digit api_key, 32 digit api_secret '
              'and a valid api_host entry in your config file.')
        # grab the configured path or use the current working directory
        repo_path = config.get("halo", "repo_base_path") or "."
        if not os.path.isdir(repo_path):
            print("Repo path does not exist or you do not have "
                  "rights to access it.")
            sane = False
    except configparser.NoOptionError as noe:
        sane = False
        print('The configuration file is malformed or missing a value.')
        print(noe._get_message())
    except configparser.Error as e:
        sane = False
        print(e._get_message())
    return sane


def sane(config):
    if not check_path(config.get('halo', 'repo_base_path')):
        sys.exit("The repository base path either does not "
                 "exist or you do not have access. Check the value in "
                 "your config file's repo_base_path setting.")
    # Check the information in config file
    if not check_config(config):
        sys.exit(
            "Error message: Please make sure you have"
            "filled all the required information in config file")
    return True
