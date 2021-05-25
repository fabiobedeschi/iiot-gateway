from os import getenv
from typing import Optional

from flask import Blueprint, jsonify, render_template, request
from flask_accept import accept, accept_fallback

from .database import Database
from .telemetry import push_user_telemetry, push_waste_bin_telemetry


class GatewayServer:
    def __init__(self, db: Optional[Database] = None, telemetry: bool = True):
        self.db = db or Database()
        self.telemetry = telemetry

    def before_request(self):
        if not (self.db and self.db.connection):
            self.db = Database()

    def find_all_users(self):
        result = self.db.find_all_users()
        return result, 200

    def find_user(self, uuid):
        result = self.db.find_user(uuid)
        return result, 200 if result else 404

    def update_user(self, uuid, data):
        if not (data and data.get('delta')):
            return None, 400

        result = self.db.update_user(
            uuid=uuid,
            delta=data.get('delta')
        )
        if result:
            if self.telemetry:
                push_user_telemetry(user=result)
            return result, 200
        else:
            return None, 404

    def find_all_waste_bins(self):
        result = self.db.find_all_waste_bins()
        return result, 200

    def find_all_waste_bins_html(self):
        result = self.db.find_all_waste_bins()
        return render_template('table_collection.html', title='Waste bins', name='waste_bins', collection=result)

    def find_waste_bin(self, uuid):
        result = self.db.find_waste_bin(uuid)
        return result, 200 if result else 404

    def update_waste_bin(self, uuid, data):
        if not (data and data.get('fill_level')):
            return None, 400

        result = self.db.update_waste_bin(
            uuid=uuid,
            fill_level=data.get('fill_level'),
        )
        if result:
            if self.telemetry:
                push_waste_bin_telemetry(waste_bin=result)
            return result, 200
        else:
            return None, 404


# Flask blueprint initialization
server_blueprint = Blueprint('server', __name__)

# Global variables
server: Optional[GatewayServer] = None


@server_blueprint.before_request
def before_request():
    global server
    if not server:
        telemetry = True
        if 'true' == getenv('DISABLE_TELEMETRY', 'false'):
            telemetry = False
        server = GatewayServer(telemetry=telemetry)
    server.before_request()


@server_blueprint.route('/')
@accept('text/html')
def root_page():
    return render_template('root.html')


@server_blueprint.route('/users', methods=['GET'])
@accept_fallback
def find_all_users():
    result, code = server.find_all_users()
    return jsonify(result), code


@find_all_users.support('text/html')
def find_all_users_html():
    return render_template('table_collection.html', title='Users', name='users', collection=server.find_all_users()[0])


@server_blueprint.route('/users/<string:uuid>', methods=['GET'])
def find_user(uuid):
    result, code = server.find_user(uuid)
    return jsonify(result), code


@server_blueprint.route('/users/<string:uuid>', methods=['PUT', 'PATCH'])
def update_user(uuid):
    result, code = server.update_user(uuid, request.json)
    return jsonify(result), code


@server_blueprint.route('/waste_bins', methods=['GET'])
@accept_fallback
def find_all_waste_bins():
    result, code = server.find_all_waste_bins()
    return jsonify(result), code


@find_all_waste_bins.support('text/html')
def find_all_waste_bins_html():
    return render_template('table_collection.html', title='Waste bins', name='waste_bins',
                           collection=server.find_all_waste_bins()[0])


@server_blueprint.route('/waste_bins/<string:uuid>', methods=['GET'])
def find_waste_bin(uuid):
    result, code = server.find_waste_bin(uuid)
    return jsonify(result), code


@server_blueprint.route('/waste_bins/<string:uuid>', methods=['PUT', 'PATCH'])
def update_waste_bin(uuid):
    result, code = server.update_waste_bin(uuid, request.json)
    return jsonify(result), code
