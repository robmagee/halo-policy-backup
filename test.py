import unittest
import os
import api
import shutil
from os import path
from six.moves import configparser
from shutil import rmtree

import fn
import sanity
from sys import stdout

class LocalTest(unittest.TestCase):
    '''
    Tests the non-API aspects of the tool.
    '''
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.key = None
        self.secret = None
        
    def setUp(self):
        '''
        Create the test directory.
        '''
        try:
            curmask = os.umask(0)
            os.makedirs(
                path.abspath(self.sane_config.get('halo', 'repo_base_path')),
                0o770)
        except os.error as oe:
            print(oe.strerror)
            sane = False
        finally:
            os.umask(curmask)
        self.key = os.environ.get('APIKEY')
        print(self.key)
        self.secret = os.environ.get('APISECRET')
        print(self.secret)

    def tearDown(self):
        '''
        Get rid of any garbage
        '''
        # get rid of any garbage
        rmtree(self.sane_config.get('halo', 'repo_base_path'))

    @property
    def sane_config(self):
        config = configparser.ConfigParser()
        config.add_section('halo')
        config.set('halo', 'api_host', 'api.cloudpassage.com')
        config.set('halo', 'api_key', '12345678')
        config.set('halo', 'api_secret', '12345678901234567890123456789012')
        config.set('halo', 'repo_base_path', './testdata')
        config.set('halo', 'repo_commit_comment', 'Unit Test')
        config.set('halo', 'proxy_host', '')
        config.set('halo', 'proxy_port', '')
        return config

    def test_sane_config(self):
        '''
        Makes sure sane configs are sane...
        '''
        self.assertTrue(sanity.check_config(self.sane_config),
                        'Sanity check failed for the sane config.')

    def test_insane_configs(self):
        '''
        Check insane configs and make sure they fail.
        '''
        config = self.sane_config
        config.set('halo', 'api_key', '123456789')
        self.assertFalse(sanity.check_config(config),
                         'Bad api_key length was accepted.')
        config = self.sane_config
        config.set(
            'halo',
            'api_secret',
            '123456789012345678asdf90123456789012')
        self.assertFalse(sanity.check_config(config),
                         'Bad api_key length was accepted.')
        config = self.sane_config
        config.set('halo', 'api_host', 'www.google.com')
        self.assertFalse(sanity.check_config(config),
                         'Bad api host was accepted.')
        config = self.sane_config
        config.set('halo', 'repo_base_path', '/asdf_zzzz')
        self.assertFalse(sanity.check_config(config),
                         'Bad repo_base_path was accepted.')

    def test_check_path(self):
        '''
        Ensures paths can be created along with the git repo.
        '''
        hsection = self.sane_config._sections['halo']
        result = sanity.check_path(hsection['repo_base_path'])
        self.assertTrue(result,
                        'The repo_base_path check failed.')

    def test_localcommit(self):
        '''
        Ensure the local commit can happen.
        '''
        repo_base_path = path.abspath(
            self.sane_config.get(
                'halo',
                'repo_base_path'))
        sanity.check_path(repo_base_path)
        paths = [path.join(repo_base_path, x)
                 for x in ("fim",
                           "csm",
                           "firewall",
                           "lids")]
        # create some junk files to commit
        for p in paths:
            f = open(path.join(p, 'test.txt'), 'w')
            f.write('halo')
            f.close()
        fn.localcommit(repo_base_path)
        fn.remotepush(repo_base_path, 'Halo Policy Backup Unit Test')

    @property
    def auth_token(self):
        token = api.get_auth_token(self.sane_config.get('halo', 'api_host'), self.key, 
            self.secret)
        self.assertIsNotNone(token, 'Could not exectue the API using '
            'the key, secret and host provided.')
        return token

    def test_get_auth_token(self):
        '''
        Ensure that they auth token for further API calls can
        be retrieved.
        '''
        if self.secret:
            print('Key and Secret provided.  Executing call '
            'to get auth token.')
            self.auth_token
        else:
            print('API Tests not available- no key or secret. Assign'
                  ' to the APIKEY and APISECRET environment variables '
                  'for use.')
             

    @property
    def policies(self):
        dsection = self.sane_config._sections['halo']
        dsection['auth_token'] = self.auth_token
        infobundle = fn.get_all_policies(*[dsection[x] for x in 
                ("api_host", "auth_token", 
                    "proxy_host", "proxy_port")])
        self.assertIsNotNone(infobundle, 'Could not execute the '
            'get policy data apis.')
        return infobundle

    def test_get_policies(self):
        '''
        Run the list of policies to backup
        '''
        if self.secret:
            infobundle = self.policies
            return infobundle
            
    def test_get_policy_data(self):
        '''
        Back up the appropriate policies.
        '''
        if self.secret:
            hsection = self.sane_config._sections['halo']
            sanity.check_path(hsection['repo_base_path'])
            dsection = self.sane_config._sections['halo']
            dsection['auth_token'] = self.auth_token
            fn.get_specific(
            dsection["api_host"],
            dsection["auth_token"],
            dsection["repo_base_path"] or ".",
            self.policies,
            dsection["proxy_host"],
            dsection["proxy_port"],
            )

suite = unittest.TestLoader().loadTestsFromTestCase(LocalTest)
suite.sortTestMethodsUsing = None

if __name__ == '__main__':
    unittest.main()
