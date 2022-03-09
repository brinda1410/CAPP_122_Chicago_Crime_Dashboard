'''
This module is run in bash to generate an instance of the
dashboard app using dash package in python.

Run this command in bash: python3 app.py
'''

from maindash import app
from viz2 import make_layout
import webbrowser
from threading import Timer

# Specify the port for url

port = 8050

if __name__ == '__main__':
    app.layout = make_layout()
    Timer(1, webbrowser.open_new("http://localhost:{}".format(port))).start();
    app.run_server(debug=False, port=port)