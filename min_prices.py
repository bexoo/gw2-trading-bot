import requests
import json
import sqlite3
import time
import datetime


def updateMinPrices():
    conn = sqlite3.connect("gw2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tp")
    items = cursor.fetchall()
    for item in items:
        id = item[0]
        if item[10] is not None:
            print(id, item[10])
            continue
        print(id)
        res = requests.get("https://api.guildwars2.com/v2/items/" + str(id))
        response = json.loads(res.text)
        min_price = response["vendor_value"]
        print(f"min price: {min_price}")
        cursor.execute(
            "update tp set MinPrice=? where ItemID=?",
            (
                min_price,
                id,
            ),
        )


if __name__ == "__main__":
    updateMinPrices()
