
from flask import Flask, jsonify, request


app = Flask(__name__)

# Sample data: DRINK MENU
menu = [
    {"id": 1, "name": "Amstel", "price": 5.0},
    {"id": 2, "name": "Hansa", "price": 6.5},
    {"id": 3, "name": "Black Label", "price": 5.0},
]

# Empty list to store orders
orders = []

# Home route 
@app.route('/')
def home():
    return "Welcome to our bar!"

# GET endpoint: fetch the menu
@app.route('/menu', methods = ['GET'])
def get_menu():
    return jsonify(menu)

# POST endpoint: create a new order 
@app.route('/order', methods=['POST'])
def place_order():
    new_order = request.get_json()
    if not new_order or "name" not in new_order or "price" not in new_order:
        return jsonify({"error": "Invalid order data"}), 400
    new_order["id"] = len(orders) + 1
    orders.append(new_order)
    return jsonify({"order_id": new_order["id"]}), 201

# GET endpoint: get the bill for a specific order
@app.route('/bill/<int:order_id>', methods=['GET'])
def get_bill(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order:
        return jsonify({"order_id": order_id, "total_price": order["price"]})
    return jsonify({"error": "Order not found"}), 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

