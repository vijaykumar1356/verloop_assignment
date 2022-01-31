from flask import Flask
from flask_restful import Api

from apis import GetAddressAPI

app = Flask(__name__)
api = Api(app, prefix='/api')

api.add_resource(
    GetAddressAPI,
    '/get_address_details',
    '/get_address_details/'
)


@app.route('/', methods=['GET'])
def index():
    return {
        'message': 'Hello World'
    }


if __name__ == '__main__':
    app.run(debug=True)
