import sys

from myoratio import start_server

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port_parameter = int(sys.argv[1])
    else:
        port_parameter = 3300

    start_server(port_parameter)
