"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from flask import current_app as app
from flask import request
from flask_restplus import Resource

from globomap_api import exceptions as gmap_exc
from globomap_api.api.v1 import api
from globomap_api.api.v2 import facade
from globomap_api.api.v2.parsers import queries as query_parsers

ns = api.namespace(
    'queries', description='Operations related to queries')


@ns.deprecated
@ns.route('/')
class Query(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
    })
    @api.expect(query_parsers.search_query_parser)
    def get(self):
        """List all queries from DB."""

        args = query_parsers.search_query_parser.parse_args(request)

        page = args.get('page')
        per_page = args.get('per_page')

        queries = facade.list_query(page, per_page)
        return queries, 200


@ns.deprecated
@ns.route('/<key>/')
@api.doc(params={
    'key': 'Key Of Query'
})
class DocumentQuery(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    def get(self, key):
        """Get query by key."""

        try:
            res = facade.get_query(key)
            return res, 200

        except gmap_exc.DocumentNotExist as error:
            app.logger.warning(error.message)
            api.abort(404, errors=error.message)


@ns.deprecated
@ns.route('/<key>/execute')
@api.doc(params={
    'key': 'Key Of Query'
})
class ExecuteQuery(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(query_parsers.execute_query_parser)
    def get(self, key):
        """Get query by key."""

        args = query_parsers.execute_query_parser.parse_args(request)
        variable = args.get('variable')

        try:
            res = facade.execute_query(key, variable)
            return res, 200

        except gmap_exc.DocumentNotExist as error:
            app.logger.warning(error.message)
            api.abort(404, errors=error.message)
