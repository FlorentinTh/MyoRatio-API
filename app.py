from gevent import monkey

monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer

from configuration import Configuration
from src.data.emg.routes import emg
from src.data.imu.routes import imu
from src.points.routes import points
from src.report.routes import report
from src.results.routes import results

app = Flask(__name__)

app.register_blueprint(imu, url_prefix="/api/data")
app.register_blueprint(emg, url_prefix="/api/data")
app.register_blueprint(points, url_prefix="/api")
app.register_blueprint(results, url_prefix="/api")
app.register_blueprint(report, url_prefix="/api")


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
