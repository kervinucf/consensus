from server.gateways.data.router import setup_data_layer
from flask import Flask
from flask_cors import CORS

class ConsensusNode:
    app = Flask(__name__)
    server_is_alive = False
    server = None
    # host = '0.0.0.0'
    host = 'localhost'
    port = 8080

    def __init__(self):
        pass

    def addCORS(self):
        CORS(self.app)

    def setup(self):
        self.addCORS()
        data_layer = setup_data_layer()
        self.app.register_blueprint(data_layer)
        # self.app.register_blueprint(chain_layer)

    def start(self):
        self.app.run(host=self.host, port=self.port, debug=True)


if __name__ == "__main__":
    node = ConsensusNode()
    node.setup()
    node.start()
