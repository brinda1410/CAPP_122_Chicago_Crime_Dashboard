###### python3 app.py

from maindash import app
from viz2 import make_layout
import webbrowser
from threading import Timer

port = 8050

if __name__ == '__main__':
    app.layout = make_layout()
    Timer(1, webbrowser.open_new("http://localhost:{}".format(port))).start();
    app.run_server(debug=False, port=port)