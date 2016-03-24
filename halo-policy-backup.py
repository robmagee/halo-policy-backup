import getopt
import sys
import api
import fn
from sanity import sane
from argparse import ArgumentParser
from six.moves import configparser

def main(args, config):
    # get the default section from the config file
    dsection = config._sections['default']

    if sane(config):
        # Get API key, set in config structure
        dsection["auth_token"] = api.get_auth_token(
            *[dsection[x] for x in
             ("api_host", "api_key", "api_secret",
              "proxy_host", "proxy_port")])
        # Get the policy stuff
        infobundle = fn.get_all_policies(
            *[dsection[x] for x in
             ("api_host", "auth_token",
              "proxy_host", "proxy_port")])

        finalbundle = fn.get_specific(
            dsection["api_host"],
            dsection["auth_token"],
            dsection["repo_base_path"] or ".",
            infobundle,
            dsection["proxy_host"],
            dsection["proxy_port"],
            )

        # Write files to disk, return bool
        if fn.localcommit(dsection["repo_base_path"]):
            print("Updated files written to disk.")
            print(fn.remotepush(
                dsection["repo_base_path"] or ".",
                dsection["repo_commit_comment"]))
        else:
            sys.exit("Error message: Failure to write locally!")


if __name__ == "__main__":
    parser = ArgumentParser(description=(
        "The script is to backup policies from each module in Halo. "
        "It is strongly recommended that you backup your policy before/after "
        "making any changes."))
    parser.add_argument("-c", "--config-file",
                        help=("Please specify your file name, if not using the default config file "
                              "The default is config.conf - the format of your custom file should "
                              "follow that of the default config.conf file."), default="config.conf")
    args = parser.parse_args()
    config = configparser.SafeConfigParser()
    try:
        config.readfp(open(args.config_file))
    except IOError as fne:
        sys.exit('No such file: {0}'.format(args.config_file))
    main(args, config)
