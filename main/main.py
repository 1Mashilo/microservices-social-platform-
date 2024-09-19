import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

load_dotenv()

CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')