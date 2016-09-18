# Copyright 2015-2016 Brocade Communications Systems Inc
# All Rights Reserved.
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from tackerclient.common import exceptions
from tackerclient.common import utils
from tackerclient.tacker.v1_0.nfvo import vim
from tackerclient.tests.unit import test_cli10

API_VERSION = "1.0"
FORMAT = 'json'
TOKEN = 'testtoken'
ENDURL = 'localurl'


class CLITestV10VIMJSON(test_cli10.CLITestV10Base):
    _RESOURCE = 'vim'
    _RESOURCES = 'vims'

    def setUp(self):
        plurals = {'vims': 'vim'}
        super(CLITestV10VIMJSON, self).setUp(plurals=plurals)
        self.vim_project = {
            'name': 'abc', 'id': '',
            'project_domain_name': 'prj_domain_name'}
        self.auth_cred = {'username': 'xyz', 'password': '12345', 'user_id':
                          '', 'user_domain_name': 'user_domain_name'}
        self.auth_url = 'http://1.2.3.4:5000'

    def test_register_vim_all_params(self):
        cmd = vim.CreateVIM(test_cli10.MyApp(sys.stdout), None)
        name = 'my-name'
        my_id = 'my-id'
        description = 'Vim Description'
        vim_config = utils.get_file_path(
            'tests/unit/vm/samples/vim_config.yaml')
        args = [
            name,
            '--config-file', vim_config,
            '--description', description]
        position_names = ['auth_cred', 'vim_project', 'auth_url']
        position_values = [self.auth_cred, self.vim_project,
                           self.auth_url]
        extra_body = {'type': 'openstack', 'name': name,
                      'description': description, 'is_default': False}
        self._test_create_resource(self._RESOURCE, cmd, None, my_id,
                                   args, position_names, position_values,
                                   extra_body=extra_body)

    def test_register_vim_with_no_auth_url(self):
        cmd = vim.CreateVIM(test_cli10.MyApp(sys.stdout), None)
        my_id = 'my-id'
        name = 'test_vim'
        description = 'Vim Description'
        vim_config = utils.get_file_path(
            'tests/unit/vm/samples/vim_config_without_auth_url.yaml')
        args = [
            name,
            '--config-file', vim_config,
            '--description', description]
        position_names = ['auth_cred', 'vim_project', 'auth_url']
        position_values = [self.auth_cred, self.vim_project,
                           self.auth_url]
        extra_body = {'type': 'openstack', 'name': name,
                      'description': description, 'is_default': False}
        message = 'Auth URL must be specified'
        ex = self.assertRaises(exceptions.TackerClientException,
                               self._test_create_resource,
                               self._RESOURCE, cmd, None, my_id, args,
                               position_names, position_values,
                               extra_body=extra_body)
        self.assertEqual(message, ex.message)
        self.assertEqual(404, ex.status_code)

    def test_register_vim_with_mandatory_params(self):
        cmd = vim.CreateVIM(test_cli10.MyApp(sys.stdout), None)
        name = 'my-name'
        my_id = 'my-id'

        vim_config = utils.get_file_path(
            'tests/unit/vm/samples/vim_config.yaml')
        args = [
            name,
            '--config-file', vim_config,
        ]
        position_names = ['auth_cred', 'vim_project', 'auth_url']
        position_values = [
            self.auth_cred,
            self.vim_project,
            self.auth_url
        ]
        extra_body = {'type': 'openstack', 'name': name, 'is_default': False}
        self._test_create_resource(self._RESOURCE, cmd, name, my_id, args,
                                   position_names, position_values,
                                   extra_body=extra_body)

    def test_list_vims(self):
        cmd = vim.ListVIM(test_cli10.MyApp(sys.stdout), None)
        self._test_list_resources(self._RESOURCES, cmd, True)

    def test_show_vim_id(self):
        cmd = vim.ShowVIM(test_cli10.MyApp(sys.stdout), None)
        args = ['--fields', 'id', self.test_id]
        self._test_show_resource(self._RESOURCE, cmd, self.test_id, args,
                                 ['id'])

    def test_show_vim_id_name(self):
        cmd = vim.ShowVIM(test_cli10.MyApp(sys.stdout), None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(self._RESOURCE, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_update_vim(self):
        cmd = vim.UpdateVIM(test_cli10.MyApp(sys.stdout), None)
        update_config = utils.get_file_path(
            'tests/unit/vm/samples/vim_config_without_auth_url.yaml')
        my_id = 'my-id'
        key = 'config-file'
        value = str(update_config)
        extra_fields = {'vim_project': self.vim_project, 'auth_cred':
                        self.auth_cred, 'is_default': False}
        self._test_update_resource(self._RESOURCE, cmd, my_id, [my_id,
                                                                '--%s' %
                                                                key, value],
                                   extra_fields)

    def test_delete_vim(self):
        cmd = vim.DeleteVIM(test_cli10.MyApp(sys.stdout), None)
        my_id = 'my-id'
        args = [my_id]
        self._test_delete_resource(self._RESOURCE, cmd, my_id, args)
