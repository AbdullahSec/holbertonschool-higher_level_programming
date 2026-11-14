"""Extend the product page to use SQLite."""
import csv
import json
import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "products.db")

def create_database():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            category TEXT NOT NULL, price REAL NOT NULL)""")
        if connection.execute("SELECT COUNT(*) FROM Products").fetchone()[0] == 0:
            connection.executemany(
                "INSERT INTO Products VALUES (?, ?, ?, ?)",
                [(1, "Laptop", "Electronics", 799.99),
                 (2, "Coffee Mug", "Home Goods", 15.99)])

def read_sql():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(
            "SELECT id, name, category, price FROM Products ORDER BY id")]

@app.route("/products")
def products():
    source = request.args.get("source", "json")
    product_id = request.args.get("id")
    try:
        if source == "sql":
            data = read_sql()
        elif source == "json":
            with open(os.path.join(BASE_DIR, "products.json"), encoding="utf-8") as file:
                data = json.load(file)
        elif source == "csv":
            with open(os.path.join(BASE_DIR, "products.csv"), newline="", encoding="utf-8") as file:
                data = list(csv.DictReader(file))
        else:
            return render_template("product_display.html", products=[], error="Wrong source")
    except sqlite3.Error:
        return render_template("product_display.html", products=[], error="Database error")
    if product_id is not None:
        data = [row for row in data if str(row.get("id")) == product_id]
        if not data:
            return render_template("product_display.html", products=[], error="Product not found")
    return render_template("product_display.html", products=data, error=None)

if __name__ == "__main__":
    create_database()
    app.run(debug=True, port=5000)
