import os
from dotenv import load_dotenv
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from producer import publish 
from dataclasses import dataclass
from urllib.parse import quote_plus
import requests

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

# ------------------------------------------------------------------------
# Models

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

# ------------------------------------------------------------------------
# Routes

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://127.0.0.1:8000/api/user/') 
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success',
        'id': json['id']
    })

@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
def view_profile(user_id):
    try:
        # Make a request to the Django API to fetch the profile
        response = requests.get(f'http://127.0.0.1:8000/api/profiles/{user_id}/')

        if response.status_code == 200:
            profile_data = response.json()
            return jsonify(profile_data)
        else:
            return jsonify({'error': 'Profile not found'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching profile data'}), 500


# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')