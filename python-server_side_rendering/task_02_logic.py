"""Read JSON data and render an items page with Flask."""
import json
import os
from flask import Flask, render_template

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/items")
def items():
    with open(os.path.join(BASE_DIR, "items.json"), encoding="utf-8") as file:
        data = json.load(file)
    return render_template("items.html", items=data.get("items", []))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
