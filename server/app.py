#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, request
import os

# Setup database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
migrate = Migrate(app, db)
db.init_app(app)

# Setup Flask-RESTful API
api = Api(app)


@app.route('/')
def home():
    return "<h1>Welcome to the Pizza API</h1>"


# Define and register resources
class RestaurantById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(), 200

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants], 200


class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict(only=("id", "name", "ingredients")) for pizza in pizzas], 200


class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return new_restaurant_pizza.to_dict(), 201
        except ValueError as e:
            return {"errors": ["validation errors"]}, 400
        except Exception as e:
            return {"errors": str(e)}, 400


api.add_resource(RestaurantById, "/restaurants/<int:id>")
api.add_resource(Restaurants, "/restaurants")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

if __name__ == '__main__':
    app.run(port=5555, debug=True)