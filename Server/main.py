from flask import Flask, request, jsonify, session
import requests
#Flask application
app = Flask(__name__)
app.secret_key = "supersecret"
inventory = []

# HELPER FUNCTIONS
def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)

def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1

# AUTHENTICATION ROUTES
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == "benson" and password == "12345":
        session["user"] = username
        return jsonify({"message": "Login successful", "Admin": username}), 200

    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/whoami", methods=["GET"])
def whoami():
    user = session.get("user")
    if user:
        return jsonify({"logged_in": True, "user": user}), 200
    return jsonify({"logged_in": False, "error": "Not logged in"}), 401

# INVENTORY ROUTES
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify({"count": len(inventory), "inventory": inventory}), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# EXTERNAL API LOOKUP
@app.route("/search/<barcode>", methods=["GET"])
def search_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "External API error"}), 502
        result = response.json()
        if result.get("status") != 1:
            return jsonify({"error": "Product not found", "barcode": barcode}), 404
        product = result.get("product", {})
        return jsonify({
            "barcode": barcode,
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "image": product.get("image_url")
        }), 200
    except requests.RequestException:
        return jsonify({"error": "Could not connect to Open Food Facts"}), 503
# INVENTORY - CREATE
@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    barcode = data.get("code")
    quantity = data.get("quantity", 0)
    expiration = data.get("expiration")

    if not barcode:
        return jsonify({"error": "Product barcode is required"}), 400
    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be a positive number"}), 400

    product_name = data.get("name", "Unknown")
    brand = data.get("brand", "Unknown")

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 1:
                product = result.get("product", {})
                product_name = product.get("product_name", product_name)
                brand = product.get("brands", brand)
    except requests.RequestException:
        pass 
    new_item = {
        "id": get_next_id(),
        "code": barcode,
        "name": product_name,
        "brand": brand,
        "quantity": quantity,
        "expiration": expiration}
    
    inventory.append(new_item)
    return jsonify({"message": "Item created successfully", "item": new_item}), 201
# INVENTORY - UPDATE & DELETE
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json() or {}
    if "quantity" in data:
        try:
            q = int(data["quantity"])
            if q < 0:
                raise ValueError
            item["quantity"] = q
        except (ValueError, TypeError):
            return jsonify({"error": "Quantity must be positive"}), 400
    for field in ["name", "brand", "expiration", "code"]:
        if field in data:
            item[field] = data[field]
    return jsonify({"message": "Item updated successfully", "item": item}), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200

# COOKIE ROUTES
@app.route("/set_cookie", methods=["GET"])
def set_cookie():
    response = jsonify({"message": "Cookie set successfully"})
    response.set_cookie("theme", "dark")
    return response

@app.route("/get_cookie", methods=["GET"])
def get_cookie():
    theme = request.cookies.get("theme", "default")
    return jsonify({"theme": theme})

@app.route("/delete_cookie", methods=["GET"])
def delete_cookie():
    response = jsonify({"message": "Cookie deleted successfully"})
    response.delete_cookie("theme")
    return response

# HOME & ERROR HANDLERS
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Inventory Management API is running",
        "endpoints": {
            "login": "POST /login",
            "logout": "POST /logout",
            "whoami": "GET /whoami",
            "get_inventory": "GET /inventory",
            "get_item": "GET /inventory/<id>",
            "create_item": "POST /inventory",
            "update_item": "PATCH /inventory/<id>",
            "delete_item": "DELETE /inventory/<id>",
            "search_product": "GET /search/<barcode>",
            "set_cookie": "GET /set_cookie",
            "get_cookie": "GET /get_cookie",
            "delete_cookie": "GET /delete_cookie"
        }
    }), 200

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405
# RUN SERVER
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
