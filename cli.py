import requests
from colorama import init, Fore, Style


BASE_URL = "http://127.0.0.1:5000"

# Keep login cookies
session = requests.Session()


    
def show_response(response):
    print("┌────────────────────────────────────────────────────────────┐")
    print("│                      RESPONSE                              │")
    print("├────────────────────────────────────────────────────────────┤")
    print("│                                                            │")
    try:
        data = response.json()
        print("│")
        if "Admin" in data:
            print(f"│  Admin   : {data['Admin']}")
        if "message" in data:
            print(f"│  Message : {data['message']}")
        for key, value in data.items():
            if key not in ["Admin", "message"]:
                print(f"│  {key} : {value}")
    except requests.exceptions.JSONDecodeError:
        print(f"│  {response.text}")
    print("│                                                            │")
    print("└────────────────────────────────────────────────────────────┘")

def login():
    print("╔════════════════════════════════════════════════╗")
    print("║          INVENTORY MANAGEMENT SYSTEM           ║")
    print("╚════════════════════════════════════════════════╝")
    print("┌────────────────────────────────────────────────┐")
    print("│                          LOGIN                 │")
    print("├────────────────────────────────────────────────┤")
    username = input("| Username: ")
    password = input("| Password: ")
    print("│                                                │")
    print("└────────────────────────────────────────────────┘")
    try:
        response = session.post(
            f"{BASE_URL}/login",
            json={"username": username, "password": password}
        )
        show_response(response)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print()
        print("┌───────────────────────────────────────────────┐")
        print("│                 ERROR                         │")
        print("├───────────────────────────────────────────────┤")
        print("│         Could not connect to Flask server.    │")
        print("└───────────────────────────────────────────────┘")
        return False

def logout():
    response = session.post(f"{BASE_URL}/logout")
    show_response(response)

def whoami():
    response = session.get(f"{BASE_URL}/whoami")
    show_response(response)

def list_inventory():
    response = session.get(f"{BASE_URL}/inventory")
    if response.status_code != 200:
        print(Fore.RED + "Failed to fetch inventory.")
        return
    data = response.json()
    inventory = data.get("inventory", [])
    count = data.get("count", len(inventory))
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                         INVENTORY MANAGEMENT SYSTEM                                    ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    print(Fore.WHITE + "┌────┬────────────────┬────────────────┬─────────────────┬──────────┬────────────┐")
    print(Fore.WHITE + "│ ID │ NAME           │ BRAND          │ CODE            │ QUANTITY │ EXPIRATION │")
    print(Fore.WHITE + "├────┼────────────────┼────────────────┼─────────────────┼──────────┼────────────┤")
    for item in inventory:
        print(
            #< = align to the left
            #2 = make the space 2 characters wide
            Fore.WHITE +
            f"│ {str(item.get('id', '')):<2} "
            f"│ {str(item.get('name', '')):<14} "
            f"│ {str(item.get('brand', '')):<14} "
            f"│ {str(item.get('code', '')):<15} "
            f"│ {str(item.get('quantity', '')):>8} "
            f"│ {str(item.get('expiration', '')):<10} │"
        )
    print(Fore.WHITE + "└────┴────────────────┴────────────────┴─────────────────┴──────────┴────────────┘")
    print()
    print(Fore.CYAN + "┌────────────────────────────────────────────────┐")
    print(Fore.CYAN + f"│ Total Items: {count:<34}│")
    print(Fore.CYAN + "└────────────────────────────────────────────────┘")

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
    print("\nSearch Product")
    barcode = input("Enter product barcode: ")
    if not barcode:
        print("Barcode is required.")
        return
    try:
        response = session.get(f"{BASE_URL}/search/{barcode}")
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")
        return

    if response.status_code == 200:
        product = response.json()
        print("\nProduct found!")
        print("Name:", product.get("name", "Unknown"))
        print("Brand:", product.get("brand", "Unknown"))

        add = input("Add this product to inventory? (y/n): ")
        if add.lower() == "y":
            add_item(
                barcode=barcode,
                name=product.get("name"),
                brand=product.get("brand")
            )

def add_item(barcode=None, name=None, brand=None):
    print("\nAdd Item")
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

    expiration = input("Enter expiration date (YYYY-MM-DD or blank): ")
    data = {
        "code": barcode,
        "name": name,
        "brand": brand,
        "quantity": quantity
    }
    if expiration:
        data["expiration"] = expiration

    try:
        response = session.post(f"{BASE_URL}/inventory", json=data)
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")

def update_item():
    print("\nUpdate Item")
    item_id = input("Enter item ID: ")
    try:
        item_id = int(item_id)
    except ValueError:
        print("ID must be a number.")
        return

    print("Leave a field blank if you don't want to change it.")
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
        response = session.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
        show_response(response)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")

def delete_item():
    print("\nDelete Item")
    item_id = input("Enter item ID: ")
    try:
        item_id = int(item_id)
    except ValueError:
        print("ID must be a number.")
        return

    confirm = input("Are you sure you want to delete this item? (y/n): ")
    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    try:
        response = session.delete(f"{BASE_URL}/inventory/{item_id}")
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
    print("\n+--------------------------------------+")
    print("|        Inventory Management Menu      |")
    print("+--------------------------------------+")
    print("| 1. List inventory                     |")
    print("| 2. Get item                           |")
    print("| 3. Search product from API            |")
    print("| 4. Add item                           |")
    print("| 5. Update item                        |")
    print("| 6. Delete item                        |")
    print("| 7. me?                          |")
    print("| 8. Set cookie                         |")
    print("| 9. Get cookie                         |")
    print("| 10. Delete cookie                     |")
    print("| 11. Logout and exit                   |")
    print("+--------------------------------------+")

def main():
    print("\nWelcome to the Inventory Management System")
    logged_in = login()
    if not logged_in:
        print("Login failed. Program closing.")
        return

    while True:
        menu()
        choice = input("Choose an option: ")
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1-11.")

if __name__ == "__main__":
    main()
