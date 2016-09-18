# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tackerclient.tacker import v1_0 as tackerV10


_VNFFG = 'vnffg'
_NFP = 'nfp'
_SFC = 'sfc'
_FC = 'classifier'


class ListFC(tackerV10.ListCommand):
    """List FCs that belong to a given tenant."""

    resource = _FC
    list_columns = ['id', 'status', 'nfp_id', 'chain_id']


class ShowFC(tackerV10.ShowCommand):
    """Show information of a given FC."""

    resource = _FC


class ListSFC(tackerV10.ListCommand):
    """List SFCs that belong to a given tenant."""

    resource = _SFC
    list_columns = ['id', 'status', 'nfp_id']


class ShowSFC(tackerV10.ShowCommand):
    """Show information of a given SFC."""

    resource = _SFC


class ListNFP(tackerV10.ListCommand):
    """List NFPs that belong to a given tenant."""

    resource = _NFP
    list_columns = ['id', 'name', 'status', 'vnffg_id', 'path_id']


class ShowNFP(tackerV10.ShowCommand):
    """Show information of a given NFP."""

    resource = _NFP


class ListVNFFG(tackerV10.ListCommand):
    """List VNFFGs that belong to a given tenant."""

    resource = _VNFFG
    list_columns = ['id', 'name', 'description', 'status', 'vnffgd_id']


class ShowVNFFG(tackerV10.ShowCommand):
    """Show information of a given VNFFG."""

    resource = _VNFFG


class CreateVNFFG(tackerV10.CreateCommand):
    """Create a VNFFG."""

    resource = _VNFFG
    remove_output_fields = ["attributes"]

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help='Set a name for the VNFFG')
        vnffgd_group = parser.add_mutually_exclusive_group(required=True)
        vnffgd_group.add_argument(
            '--vnffgd-id',
            help='VNFFGD ID to use as template to create VNFFG')
        vnffgd_group.add_argument(
            '--vnffgd-name',
            help='VNFFGD Name to use as template to create VNFFG')
        parser.add_argument(
            '--vnf-mapping',
            help='List of logical VNFD name to VNF instance name mapping.  '
                 'Example: VNF1:my_vnf1,VNF2:my_vnf2')
        parser.add_argument(
            '--symmetrical', metavar='{True,False}',
            help='Should a reverse path be created for the NFP')

    def args2body(self, parsed_args):
        body = {self.resource: {}}

        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format

        if parsed_args.vnf_mapping:
            _vnf_mapping = dict()
            _vnf_mappings = parsed_args.vnf_mapping.split(",")
            for mapping in _vnf_mappings:
                vnfd_name, vnf = mapping.split(":", 1)
                _vnf_mapping[vnfd_name] = \
                    tackerV10.find_resourceid_by_name_or_id(
                        tacker_client, 'vnf', vnf)

            parsed_args.vnf_mapping = _vnf_mapping

        if parsed_args.vnffgd_name:
            _id = tackerV10.find_resourceid_by_name_or_id(tacker_client,
                                                          'vnffgd',
                                                          parsed_args.
                                                          vnffgd_name)
            parsed_args.vnffgd_id = _id

        tackerV10.update_dict(parsed_args, body[self.resource],
                              ['tenant_id', 'name', 'vnffgd_id',
                               'symmetrical', 'vnf_mapping'])
        return body


class UpdateVNFFG(tackerV10.UpdateCommand):
    """Update a given VNFFG."""

    resource = _VNFFG

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--vnf-mapping',
            help='List of logical VNFD name to VNF instance name mapping.  '
                 'Example: VNF1:my_vnf1,VNF2:my_vnf2')
        parser.add_argument(
            '--symmetrical', metavar='{True,False}',
            help='Should a reverse path be created for the NFP')

    def args2body(self, parsed_args):
        body = {self.resource: {}}

        tacker_client = self.get_client()
        tacker_client.format = parsed_args.request_format

        if parsed_args.vnf_mapping:
            _vnf_mapping = dict()
            _vnf_mappings = parsed_args.vnf_mapping.split(",")
            for mapping in _vnf_mappings:
                vnfd_name, vnf = mapping.split(":", 1)
                _vnf_mapping[vnfd_name] = \
                    tackerV10.find_resourceid_by_name_or_id(
                        tacker_client, 'vnf', vnf)

            parsed_args.vnf_mapping = _vnf_mapping

        tackerV10.update_dict(parsed_args, body[self.resource],
                              ['tenant_id', 'vnf_mapping', 'symmetrical'])
        return body


class DeleteVNFFG(tackerV10.DeleteCommand):
    """Delete a given VNFFG."""

    resource = _VNFFG
