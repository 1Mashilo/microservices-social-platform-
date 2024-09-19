import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

app = Flask(__name__)

load_dotenv()

quoted_password = quote_plus(os.getenv("MYSQL_PASSWORD"))
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{quoted_password}@" 
    f"{os.getenv('MYSQL_DB_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
)

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')