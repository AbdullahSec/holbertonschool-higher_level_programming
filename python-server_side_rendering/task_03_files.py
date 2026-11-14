"""Display products from JSON or CSV files."""
import csv
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_json():
    with open(os.path.join(BASE_DIR, "products.json"), encoding="utf-8") as file:
        return json.load(file)

def read_csv():
    with open(os.path.join(BASE_DIR, "products.csv"), newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

@app.route("/products")
def products():
    source = request.args.get("source", "json")
    product_id = request.args.get("id")
    if source == "json":
        data = read_json()
    elif source == "csv":
        data = read_csv()
    else:
        return render_template("product_display.html", products=[], error="Wrong source")
    if product_id is not None:
        data = [row for row in data if str(row.get("id")) == product_id]
        if not data:
            return render_template("product_display.html", products=[], error="Product not found")
    return render_template("product_display.html", products=data, error=None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
