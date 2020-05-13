# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.resource import Resource, ResourcePatchMixin, ResourceHelper
from hpOneView.resources.settings.scopes import Scopes


class ScopesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = Scopes(oneview_connection)


    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        sort = 'name:ascending'
        query = 'name eq "TestName"'
        view = 'expand'

        self.resource.get_all(2, 500, sort, query, view)
        mock_get_all.assert_called_once_with(2, 500, sort=sort, query=query, view=view)


    @mock.patch.object(Resource, 'update')
    def test_update_called_once(self, mock_update):
        data = {
            'name': 'Name of the Scope',
            'uri': 'a_uri'
        }
        data_rest_call = data.copy()

        self.resource.update(data, 60)

        headers = {'If-Match': '*'}
        mock_update.assert_called_once_with(data_rest_call, timeout=60,
                                            default_values=self.resource.DEFAULT_VALUES,
                                            custom_headers=headers)

    @mock.patch.object(Resource, 'update')
    def test_update_should_verify_if_match_etag_when_provided(self, mock_update):
        data = {'eTag': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}

        self.resource.update(data, -1)

        headers = {'If-Match': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}
        mock_update.assert_called_once_with(mock.ANY, timeout=mock.ANY, default_values=mock.ANY,
                                            custom_headers=headers)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self.resource.delete(id, timeout=-1)

        mock_delete.assert_called_once_with(id, timeout=-1, custom_headers={'If-Match': '*'})

    @mock.patch.object(Resource, 'delete')
    def test_delete_should_verify_if_match_etag_when_provided(self, mock_delete):
        data = {'uri': 'a_uri',
                'eTag': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}

        self.resource.delete(data, -1)

        headers = {'If-Match': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}
        mock_delete.assert_called_once_with(mock.ANY, timeout=mock.ANY, custom_headers=headers)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_update_resource_assignments_called_once(self, mock_patch_request):
        uri = '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2'

        information = {
            "addedResourceUris": ["/rest/ethernet-networks/e801b73f-b4e8-4b32-b042-36f5bac2d60f"],
            "removedResourceUris": ["/rest/ethernet-networks/390bc9f9-cdd5-4c70-b38f-cf04e64f5c72"]
        }
        self.resource.update_resource_assignments(uri, information, timeout=-1)

        mock_patch_request.assert_called_once_with(
            '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2/resource-assignments',
            information.copy(),
            timeout=-1)

