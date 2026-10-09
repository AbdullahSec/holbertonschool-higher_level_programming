import csv
import json


def convert_csv_to_json(csv_filename):
    try:
        with open(csv_filename, "r", encoding="utf-8") as csv_file:
            data = list(csv.DictReader(csv_file))

        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file)

        return True
    except FileNotFoundError:
        return False
