import sqlite3
import requests
import json

# TODO: Use the number of listings to calculate how many items to buy/sell


def getTarget():
    conn = sqlite3.connect("gw2.db")
    cursor = conn.cursor()
    # Need to check if FlipIndex is the right column name
    cursor.execute("SELECT * FROM tp ORDER BY FlipIndex DESC LIMIT 1")
    items = cursor.fetchall()
    target = items[0][0]
    # I want to get the item with the highest "FlipIndex" value

    conn.close()
    return target


def getTotalListings(target):
    res = requests.get(f"https://api.guildwars2.com/v2/commerce/listings/{target}")
    response = json.loads(res.text)
    listings = {"buys": 0, "sells": 0}
    for row in response["buys"]:
        listings["buys"] += row["listings"]
    for row in response["sells"]:
        listings["sells"] += row["listings"]

    return listings


if __name__ == "__main__":
    target = getTarget()
    print(target)
    listings = getTotalListings(target)

    print(listings)
