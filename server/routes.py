from models import db, Restaurant

# Example: GET /restaurants/<int:id>
class RestaurantResource(Resource):
    def get(self, id):
        # Use db.session.get instead of query.get
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(), 200

    def delete(self, id):
        # Use db.session.get instead of query.get
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204