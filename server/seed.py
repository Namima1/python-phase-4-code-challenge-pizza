#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Main St")
    bistro = Restaurant(name="Sanjay's Pizza", address="456 Elm St")
    palace = Restaurant(name="Kiki's Pizza", address="789 Oak St")

    print("Creating pizzas...")
    cheese = Pizza(name="Cheese Pizza", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Pepperoni Pizza", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    veggie = Pizza(name="Veggie Pizza", ingredients="Dough, Tomato Sauce, Cheese, Veggies")

    print("Creating restaurant-pizza relationships...")
    rp1 = RestaurantPizza(price=10, restaurant=shack, pizza=cheese)
    rp2 = RestaurantPizza(price=12, restaurant=bistro, pizza=pepperoni)
    rp3 = RestaurantPizza(price=15, restaurant=palace, pizza=veggie)

    db.session.add_all([shack, bistro, palace, cheese, pepperoni, veggie, rp1, rp2, rp3])
    db.session.commit()
    print("Seeding completed!")