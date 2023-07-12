import sys

from gevent import monkey

monkey.patch_all()

from dotenv import dotenv_values  # noqa: E402
from flask import Flask  # noqa: E402
from gevent.pywsgi import WSGIServer  # noqa: E402

from myoratio.api.routes import api_blueprint  # noqa: E402
from myoratio.data.emg.routes import emg_blueprint  # noqa: E402
from myoratio.data.imu.routes import imu_blueprint  # noqa: E402
from myoratio.points.routes import points_blueprint  # noqa: E402
from myoratio.report.routes import report_blueprint  # noqa: E402
from myoratio.results.routes import results_blueprint  # noqa: E402

configuration = dotenv_values(".env")

app = Flask(__name__)

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(imu_blueprint, url_prefix="/api/data")
app.register_blueprint(emg_blueprint, url_prefix="/api/data")
app.register_blueprint(points_blueprint, url_prefix="/api")
app.register_blueprint(results_blueprint, url_prefix="/api")
app.register_blueprint(report_blueprint, url_prefix="/api")


def start_server(port: int) -> None:
    with WSGIServer((configuration["HOST"], port), app, backlog=2048) as http:
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.stop()


def run():
    if len(sys.argv) > 1:
        port_parameter = int(sys.argv[1])
    else:
        port_parameter = 3300

    start_server(port_parameter)
