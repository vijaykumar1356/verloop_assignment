import os
from dicttoxml import dicttoxml
import requests
from flask import Response
from flask_restful import Resource, fields, reqparse, marshal, abort as api_abort

parser = reqparse.RequestParser()
parser.add_argument('address', type=str, required=True, location='json')
parser.add_argument('output_format', type=str, required=True, location='json')

output_fields = {
    'address': fields.String,
    'coordinates': fields.Raw
}


class GetAddressAPI(Resource):
    def get(self):
        return {
            'message': 'Hello, This is a GET request'
        }

    def post(self):
        API_KEY = os.environ.get('API_KEY')
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        post_data = parser.parse_args()
        if not post_data['output_format'].lower() in ['json', 'xml']:
            api_abort(400, message='please provide a proper output format i.e., XML or JSON')
        params = {
            'address': post_data['address'],
            'key': API_KEY
        }
        response = requests.get(base_url, params=params)
        data = response.json()['results'][0]
        output_data = {
            "address": data['formatted_address'],
            "coordinates": data['geometry']['location']
        }
        if post_data.get('output_format').lower() == 'xml':
            xml_data = dicttoxml(output_data)
            response = Response(response=xml_data, status=200, mimetype='application/xml')
            return response
        return marshal(output_data, output_fields)
