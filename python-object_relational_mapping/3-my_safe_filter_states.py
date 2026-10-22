#!/usr/bin/python3
"""Filter states with a bound parameter."""

import sys

import MySQLdb


if __name__ == "__main__":
    connection = MySQLdb.connect(
        host="localhost", port=3306,
        user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3]
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM states WHERE name = %s ORDER BY id ASC",
        (sys.argv[4],)
    )
    for state in cursor.fetchall():
        print(state)
    cursor.close()
    connection.close()
