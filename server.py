import sys

from gevent import monkey

monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer

from configuration import Configuration
from myoratio.api.routes import api_blueprint
from myoratio.data.emg.routes import emg_blueprint
from myoratio.data.imu.routes import imu_blueprint
from myoratio.points.routes import points_blueprint
from myoratio.report.routes import report_blueprint
from myoratio.results.routes import results_blueprint

app = Flask(__name__)

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(imu_blueprint, url_prefix="/api/data")
app.register_blueprint(emg_blueprint, url_prefix="/api/data")
app.register_blueprint(points_blueprint, url_prefix="/api")
app.register_blueprint(results_blueprint, url_prefix="/api")
app.register_blueprint(report_blueprint, url_prefix="/api")


def start_server(port: int) -> None:
    with WSGIServer(
        (Configuration.HOST.value, port),
        app,
        backlog=2048,
    ) as http:
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.stop()


if __name__ == "__main__":
    if sys.argv[1] is not None:
        port_parameter = int(sys.argv[1])
    else:
        port_parameter = 3300

    start_server(port_parameter)
