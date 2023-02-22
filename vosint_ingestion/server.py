from flask import Flask, jsonify, make_response
from flask_cors import CORS

from common import InternalError
from logger import Logger
from configs import GlobalConfigs
from router import register_routes


# Create Flask application
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Router register
register_routes(app)


@app.route('/')
def index():
    return '''<h3>VOSINT Ingestion API</h3>'''


@app.errorhandler(InternalError)
def internal_exception_hander(error: InternalError):
    Logger.instance().error(error)

    return make_response(
        jsonify({
            'success': False,
            'error': error.to_dict()
        })
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=GlobalConfigs.instance().API['port'],
            threaded=True,
            debug=True)
