#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_array = []
    bakeries = Bakery.query.all()
    for bakery in bakeries:
        bakery_array.append(bakery.to_dict())
    return make_response(bakery_array, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    body = ""
    status = ""
    if bakery:
        body = bakery.to_dict()
        status = 200
    else:
        body = f"Error retrieving bakery by bakery id:{id}"
        status = 404 
    return make_response(body, 200)
    
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    array = []
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    for goods in baked_goods:
        array.append(goods.to_dict())
    return make_response(array, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(most_expensive.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)