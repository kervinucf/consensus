from flask import Blueprint, jsonify
from server.gateways.data.routes.earthcam import cams
from server.gateways.data.routes.finance import finance
from server.gateways.data.routes.geo import geo
from server.gateways.data.routes.sports import sports
from server.gateways.data.routes.twitter import twitter
from server.gateways.data.routes.weather import weather


def setup_data_layer():
    data_layer = Blueprint('data', __name__, url_prefix="/data")
    data_layer.register_blueprint(cams)
    data_layer.register_blueprint(finance)
    data_layer.register_blueprint(geo)
    data_layer.register_blueprint(sports)
    data_layer.register_blueprint(weather)
    # data_layer.register(news)
    # data_layer.register(music)
    data_layer.register_blueprint(twitter)
    return data_layer



