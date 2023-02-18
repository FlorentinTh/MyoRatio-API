from gevent import monkey

monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer

from configuration import Configuration
from emgtrigno.data.emg.routes import emg_blueprint
from emgtrigno.data.imu.routes import imu_blueprint
from emgtrigno.points.routes import points_blueprint
from emgtrigno.report.routes import report_blueprint
from emgtrigno.results.routes import results_blueprint

app = Flask(__name__)

app.register_blueprint(imu_blueprint, url_prefix="/api/data")
app.register_blueprint(emg_blueprint, url_prefix="/api/data")
app.register_blueprint(points_blueprint, url_prefix="/api")
app.register_blueprint(results_blueprint, url_prefix="/api")
app.register_blueprint(report_blueprint, url_prefix="/api")


def start_server():
    with WSGIServer(
        (Configuration.HOST.value, Configuration.PORT.value),
        app,
        backlog=2048,
    ) as http:
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.stop()


if __name__ == "__main__":
    start_server()
