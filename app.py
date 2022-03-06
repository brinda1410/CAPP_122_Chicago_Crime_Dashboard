###### python3 app.py

from maindash import app
from viz2 import make_layout

if __name__ == '__main__':
    app.layout = make_layout()
    app.run_server(debug=True)