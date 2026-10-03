import requests

BASE_URL = "http://127.0.0.1:5000"

# Keep login cookies
session = requests.Session()

def show_response(response):
    print()
    print("=" * 40)
    print("STATUS:", response.status_code)
    print("=" * 40)
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print(response.text)
    print("=" * 40)

def login():
    print("\n========== LOGIN ==========")
    username = input("Username: ")
    password = input("Password: ")
    try:
        response = session.post(
            f"{BASE_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )
        show_response(response)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")
        print("Make sure main.py is running.")
        return False

def logout():
    response = session.post(f"{BASE_URL}/logout")
    show_response(response)

def whoami():
    response = session.get(f"{BASE_URL}/whoami")
    show_response(response)

def list_inventory():
    response = session.get(f"{BASE_URL}/inventory")
    show_response(response)

def get_item():
    item_id = input("Enter item ID: ")
    try:
        item_id = int(item_id)
    except ValueError:
        print("ID must be a number.")
        return
    response = session.get(f"{BASE_URL}/inventory/{item_id}")
    show_response(response)

def search_product():
    print("\n========== SEARCH PRODUCT ==========")
    barcode = input("Enter product barcode: ")
    if not barcode:
        print("Barcode is required.")
        return
    try:
        response = session.get(
            f"{BASE_URL}/search/{barcode}"
        )
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")
        return
    if response.status_code == 200:
        product = response.json()

        print("\nProduct found!")
        print("Name:", product.get("name", "Unknown"))
        print("Brand:", product.get("brand", "Unknown"))

        add = input("\nAdd this product to inventory? (y/n): ")

        if add.lower() == "y":
            add_item(
                barcode=barcode,
                name=product.get("name"),
                brand=product.get("brand")
            )
def add_item(barcode=None, name=None, brand=None):
    print("\n========== ADD ITEM ==========")
    if barcode is None:
        barcode = input("Enter product barcode: ")
    if not barcode:
        print("Barcode is required.")
        return
    if name is None:
        name = input("Enter product name: ")
    if brand is None:
        brand = input("Enter brand: ")
    quantity = input("Enter quantity: ")
    try:
        quantity = int(quantity)

        if quantity < 0:
            print("Quantity cannot be negative.")
            return
    except ValueError:
        print("Quantity must be a number.")
        return
    expiration = input(
        "Enter expiration date (YYYY-MM-DD or blank): "
    )
    data = {
        "code": barcode,
        "name": name,
        "brand": brand,
        "quantity": quantity
    }
    if expiration:
        data["expiration"] = expiration
    try:
        response = session.post(
            f"{BASE_URL}/inventory",
            json=data
        )

        show_response(response)

    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")
def update_item():
    print("\n========== UPDATE ITEM ==========")
    item_id = input("Enter item ID: ")
    try:
        item_id = int(item_id)
    except ValueError:
        print("ID must be a number.")
        return
    print("\nLeave a field blank if you don't want to change it.")

    quantity = input("New quantity: ")
    name = input("New name: ")
    brand = input("New brand: ")
    expiration = input("New expiration: ")
    data = {}
    if quantity:
        try:
            data["quantity"] = int(quantity)
            if data["quantity"] < 0:
                print("Quantity cannot be negative.")
                return
        except ValueError:
            print("Quantity must be a number.")
            return
    if name:
        data["name"] = name
    if brand:
        data["brand"] = brand
    if expiration:
        data["expiration"] = expiration
    if not data:
        print("Nothing to update.")
        return
    try:
        response = session.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=data
        )
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")

def delete_item():
    print("\n========== DELETE ITEM ==========")

    item_id = input("Enter item ID: ")

    try:
        item_id = int(item_id)
    except ValueError:
        print("ID must be a number.")
        return
    confirm = input(
        "Are you sure you want to delete this item? (y/n): "
    )
    if confirm.lower() != "y":
        print("Delete cancelled.")
        return
    try:
        response = session.delete(
            f"{BASE_URL}/inventory/{item_id}"
        )
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")
def set_cookie():
    response = session.get(f"{BASE_URL}/set_cookie")
    show_response(response)
def get_cookie():
    response = session.get(f"{BASE_URL}/get_cookie")
    show_response(response)
def delete_cookie():
    response = session.get(f"{BASE_URL}/delete_cookie")
    show_response(response)
def menu():
    print("\n========== INVENTORY MANAGEMENT ==========")
    print("1. List inventory")
    print("2. Get item")
    print("3. Search product")
    print("4. Add item")
    print("5. Update item")
    print("6. Delete item")
    print("7. Who am I?")
    print("8. Set cookie")
    print("9. Get cookie")
    print("10. Delete cookie")
    print("11. Logout and exit")
    print("===========================================")

def main():
    print("\n================================")
    print("   INVENTORY MANAGEMENT SYSTEM")
    print("================================")
    logged_in = login()
    if not logged_in:
        print("\nLogin failed.")
        print("Program closing.")
        return

    while True:
        menu()
        choice = input("\nChoose an option: ")
        if choice == "1":
            list_inventory()
        elif choice == "2":
            get_item()
        elif choice == "3":
            search_product()
        elif choice == "4":
            add_item()
        elif choice == "5":
            update_item()
        elif choice == "6":
            delete_item()
        elif choice == "7":
            whoami()
        elif choice == "8":
            set_cookie()
        elif choice == "9":
            get_cookie()
        elif choice == "10":
            delete_cookie()
        elif choice == "11":
            logout()
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please choose 1-11.")
if __name__ == "__main__":
    main()
