#
# Copyright 2013 Intel Corporation
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

import yaml

from tackerclient.common import utils
from tackerclient.i18n import _
from tackerclient.tacker import v1_0 as tackerV10


_VNF = 'vnf'
_RESOURCE = 'resource'


class ListVNF(tackerV10.ListCommand):
    """List VNF that belong to a given tenant."""

    resource = _VNF
    list_columns = ['id', 'name', 'description', 'mgmt_url', 'status',
                    'vim_id', 'placement_attr', 'error_reason']


class ShowVNF(tackerV10.ShowCommand):
    """Show information of a given VNF."""

    resource = _VNF


class CreateVNF(tackerV10.CreateCommand):
    """Create a VNF."""

    resource = _VNF
    remove_output_fields = ["attributes"]

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help='Set a name for the VNF')
        parser.add_argument(
            '--description',
            help='Set description for the VNF')
        vnfd_group = parser.add_mutually_exclusive_group(required=True)
        vnfd_group.add_argument(
            '--vnfd-id',
            help='VNFD ID to use as template to create VNF')
        vnfd_group.add_argument(
            '--vnfd-name',
            help='VNFD Name to use as template to create VNF')
        vim_group = parser.add_mutually_exclusive_group()
        vim_group.add_argument(
            '--vim-id',
            help='VIM ID to use to create VNF on the specified VIM')
        vim_group.add_argument(
            '--vim-name',
            help='VIM name to use to create VNF on the specified VIM')
        parser.add_argument(
            '--vim-region-name',
            help='VIM Region to use to create VNF on the specified VIM')
        parser.add_argument(
            '--config-file',
            help='Specify config yaml file')
        parser.add_argument(
            '--config',
            help='Specify config yaml data')
        parser.add_argument(
            '--param-file',
            help='Specify parameter yaml file'
        )

    def args2body(self, parsed_args):
        args = {'attributes': {}}
        body = {self.resource: args}
        # config arg passed as data overrides config yaml when both args passed
        config = None
        if parsed_args.config_file:
            with open(parsed_args.config_file) as f:
                config_yaml = f.read()
            config = yaml.load(
                config_yaml, Loader=yaml.SafeLoader)
        if parsed_args.config:
            config = parsed_args.config
            if isinstance(config, str):
                config_str = parsed_args.config.decode('unicode_escape')
                config = yaml.load(config_str, Loader=yaml.SafeLoader)
                utils.deprecate_warning(what='yaml as string', as_of='N',
                                        in_favor_of='yaml as dictionary')

        if config:
            args['attributes']['config'] = config
        if parsed_args.vim_region_name:
            args.setdefault('placement_attr', {})['region_name'] = \
                parsed_args.vim_region_name

        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format
        if parsed_args.vim_name:
                _id = tackerV10.find_resourceid_by_name_or_id(tacker_client,
                                                              'vim',
                                                              parsed_args.
                                                              vim_name)
                parsed_args.vim_id = _id
        if parsed_args.vnfd_name:
                _id = tackerV10.find_resourceid_by_name_or_id(tacker_client,
                                                              'vnfd',
                                                              parsed_args.
                                                              vnfd_name)
                parsed_args.vnfd_id = _id
        if parsed_args.param_file:
            with open(parsed_args.param_file) as f:
                param_yaml = f.read()
            args['attributes']['param_values'] = yaml.load(
                param_yaml, Loader=yaml.SafeLoader)
        tackerV10.update_dict(parsed_args, body[self.resource],
                              ['tenant_id', 'name', 'description',
                               'vnfd_id', 'vim_id'])
        return body


class UpdateVNF(tackerV10.UpdateCommand):
    """Update a given VNF."""

    resource = _VNF

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--config-file',
            help='Specify config yaml file')
        parser.add_argument(
            '--config',
            help='Specify config yaml data')

    def args2body(self, parsed_args):
        body = {self.resource: {}}
        # config arg passed as data overrides config yaml when both args passed
        config = None
        if parsed_args.config_file:
            with open(parsed_args.config_file) as f:
                config_yaml = f.read()
            config = yaml.load(config_yaml, Loader=yaml.SafeLoader)
        if parsed_args.config:
            config = parsed_args.config
            if isinstance(parsed_args.config, str):
                config_str = parsed_args.config.decode('unicode_escape')
                config = yaml.load(config_str, Loader=yaml.SafeLoader)
                utils.deprecate_warning(what='yaml as string', as_of='N',
                                        in_favor_of='yaml as dictionary')
        if config:
            body[self.resource]['attributes'] = {'config': config}
        tackerV10.update_dict(parsed_args, body[self.resource], ['tenant_id'])
        return body


class DeleteVNF(tackerV10.DeleteCommand):
    """Delete a given VNF."""

    resource = _VNF


class ListVNFResources(tackerV10.ListCommand):
    """List resources of a VNF like VDU, CP, etc."""

    list_columns = ['name', 'id', 'type']
    allow_names = True
    resource = _VNF

    def get_id(self):
        if self.resource:
            return self.resource.upper()

    def get_parser(self, prog_name):
        parser = super(ListVNFResources, self).get_parser(prog_name)
        if self.allow_names:
            help_str = _('ID or name of %s to look up')
        else:
            help_str = _('ID of %s to look up')
        parser.add_argument(
            'id', metavar=self.get_id(),
            help=help_str % self.resource)
        return parser

    def get_data(self, parsed_args):
        self.log.debug('get_data(%s)', parsed_args)
        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format
        if self.allow_names:
            _id = tackerV10.find_resourceid_by_name_or_id(tacker_client,
                                                          self.resource,
                                                          parsed_args.id)
        else:
            _id = parsed_args.id

        data = self.retrieve_list_by_id(_id, parsed_args)
        self.extend_list(data, parsed_args)
        return self.setup_columns(data, parsed_args)

    def retrieve_list_by_id(self, id, parsed_args):
        """Retrieve a list of sub resources from Tacker server"""
        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format
        _extra_values = tackerV10.parse_args_to_dict(self.values_specs)
        tackerV10._merge_args(self, parsed_args, _extra_values,
                              self.values_specs)
        search_opts = self.args2search_opts(parsed_args)
        search_opts.update(_extra_values)
        if self.pagination_support:
            page_size = parsed_args.page_size
            if page_size:
                search_opts.update({'limit': page_size})
        if self.sorting_support:
            keys = parsed_args.sort_key
            if keys:
                search_opts.update({'sort_key': keys})
            dirs = parsed_args.sort_dir
            len_diff = len(keys) - len(dirs)
            if len_diff > 0:
                dirs += ['asc'] * len_diff
            elif len_diff < 0:
                dirs = dirs[:len(keys)]
            if dirs:
                search_opts.update({'sort_dir': dirs})
        obj_lister = getattr(tacker_client, "list_vnf_resources")
        data = obj_lister(id, **search_opts)
        return data.get('resources', [])


class ScaleVNF(tackerV10.TackerCommand):
    """Scale a VNF."""

    api = 'nfv-orchestration'
    resource = None
    log = None

    def get_parser(self, prog_name):
        parser = super(ScaleVNF, self).get_parser(prog_name)
        self.add_known_arguments(parser)
        return parser

    def run(self, parsed_args):
        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format
        body = self.args2body(parsed_args)
        obj_creator = getattr(tacker_client,
                              "scale_vnf")
        obj_creator(body["scale"].pop('vnf_id'), body)

    def add_known_arguments(self, parser):
        vnf_group = parser.add_mutually_exclusive_group(required=True)
        vnf_group.add_argument(
            '--vnf-id',
            help='VNF ID')
        vnf_group.add_argument(
            '--vnf-name',
            help='VNF name')
        parser.add_argument(
            '--scaling-policy-name',
            help='VNF policy name used to scale')
        parser.add_argument(
            '--scaling-type',
            help='VNF scaling type, it could be either "out" or "in"')

    def args2body(self, parsed_args):
        args = {}
        body = {"scale": args}

        if parsed_args.vnf_name:
            tacker_client = self.get_client()
            tacker_client.format = parsed_args.request_format
            _id = tackerV10.find_resourceid_by_name_or_id(tacker_client,
                                                          'vnf',
                                                          parsed_args.
                                                          vnf_name)
            parsed_args.vnf_id = _id

        args['vnf_id'] = parsed_args.vnf_id
        args['type'] = parsed_args.scaling_type
        args['policy'] = parsed_args.scaling_policy_name

        return body
