import unittest
import sanity
import os
import shutil
from os import path
from six.moves import configparser
from shutil import rmtree


class LocalTest(unittest.TestCase):
    '''
    Tests the non-API aspects of the tool.
    '''

    def setUp(self):
        '''
        Create the test directory.
        '''
        try:
            curmask = os.umask(0)
            os.makedirs(
                self.sane_config.get('halo', 'repo_base_path'),
                0o770)
        except os.error as oe:
            print(oe.strerror)
            sane = False
        finally:
            os.umask(curmask)

    def tearDown(self):
        '''
        Get rid of any garbage
        '''
        # get rid of any garbage
        rmtree(self.sane_config.get('halo', 'repo_base_path'))

    @property
    def sane_config(self):
        config = configparser.SafeConfigParser()
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
        paths = [path.join(hsection['repo_base_path'], x)
                 for x in ("fim",
                           "csm",
                           "firewall",
                           "lids")]


if __name__ == '__main__':
    unittest.main()
