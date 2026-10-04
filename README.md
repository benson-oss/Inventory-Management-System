**Project Overview**
This is a Flask learning project designed to make web development concepts practical. It’s not just theory — you actually build a small system that teaches you how REST APIs, CRUD operations, sessions, cookies, and external APIs all fit together.

Think of it as a mini warehouse manager: you log in, manage products, look them up by barcode, and even test everything automatically.

## What the App Does
You log in with a username and password.

Once inside, you can view, add, update, or delete products in your inventory.

You can also search for real product info using the Open Food Facts API (just by entering a barcode).

The app remembers who’s logged in using sessions, and it demonstrates cookies by letting you set and read a simple “theme” preference.

All of this is controlled by a Flask REST API backend and a Python CLI frontend.

 It’s deliberately simple: instead of a database, it uses Python lists and dictionaries so you can focus on learning Flask and APIs.

## Project Structure
Code
       `Inventory-Management-System/
│
├── cli.py              # Command-line client
├── README.md
├── requirements.txt     # Dependencies
├── venv/                # Virtual environment
│
├── Server/
│   └── main.py          # Flask backend
│
└── tests/
    ├── test_api.py      # API tests
    └── test_cli.py      # CLI tests
Server/main.py → Flask app with routes, inventory, login, cookies, external API integration.

cli.py → Interactive command-line tool that talks to the Flask API.

tests/ → Automated tests using pytest.

## Running the Project
Start the Flask server (python main.py).

Open another terminal and run the CLI (python cli.py).

Log in with benson / 12345.

Use the menu to manage inventory, search products, and test cookies.
  The API runs at http://127.0.0.1:5000.

## REST API Routes
        POST /login → log in
        POST /logout → log out
        GET /whoami → check current user
        GET /inventory → list all items
        GET /inventory/<id> → get one item
        POST /inventory → add new item
        PATCH /inventory/<id> → update item
        DELETE /inventory/<id> → delete item
        GET /search/<barcode> → fetch product info from Open Food Facts
        GET /set_cookie / GET /get_cookie / GET /delete_cookie → cookie demo

## How Inventory Works
Stored in a Python list:

python
inventory = []
Each item is a dictionary:

    `json
    {
    "id": 1,
    "code": "5449000000996",
    "name": "Coca Cola",
    "brand": "Coca Cola",
    "quantity": 10,
    "expiration": "2027-01-20"
    }`
 Simple, but enough to understand CRUD before moving to databases.

## Authentication & Sessions
Login with POST /login.

Flask saves the user in session["user"].

GET /whoami shows who’s logged in.

POST /logout clears the session.

 This demonstrates how web apps remember users between requests.

## Cookies
    GET /set_cookie → sets a cookie (theme=dark).

    GET /get_cookie → reads it.

    GET /delete_cookie → removes it.

 Shows the difference between sessions (who’s logged in) and cookies (preferences stored in the browser).

## External API Integration
Enter a barcode in the CLI.

Flask calls Open Food Facts API.

Returns product info (name, brand, image).

CLI asks: “Add this product to inventory?”

If yes, it’s saved in your local inventory.

 This demonstrates how your app can consume external data and use it internally.

## CLI Menu
The CLI gives you options like:
    List inventory
    Get item
    Search product by barcode
    Add item
    Update item
    Delete item
    Who am I?
    Set cookie
    Get cookie
    Delete cookie
    Logout and exit
It’s a simple text menu that sends HTTP requests to Flask and prints JSON responses.

## Testing
Automated tests with pytest check routes and CLI commands.

Tests simulate API responses (using monkeypatch) for offline usage.

Run with:

Code
python -m pip install pytest

***source Server/venv/bin/activate**

python -m pytest -v

## Algorithms & Big O
Searching inventory by ID uses a linear search → O(n).

Direct access (like inventory[0]) is O(1).
This gives you a chance to discuss efficiency and how databases improve performance.

## Git Workflow
Work on features in branches (feature/cli, feature/tests).
Commit, push, and create Pull Requests.
Merge into main and clean up branches.
 Teaches you real-world Git practices.

