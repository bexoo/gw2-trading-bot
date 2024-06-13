import requests
import json
import sqlite3
import time
import datetime

def getPrices():
    page_count = 1
    prices = {}
    page_counter = 0

    for page_counter in range(page_count):
        count_string = str(page_counter)
        res = requests.get('https://api.guildwars2.com/v2/commerce/prices?page='+count_string+'&page_size=200')
        response = json.loads(res.text)

        if(page_counter == 0):
            page_count = res.headers['X-Page-Total']

        for j in range(200):
            id = response[j]['id']
            buy_price = response[j]['buys']['unit_price']
            buy_quantity = response[j]['buys']['quantity'] # This is the quantity for the top offer
            sell_price = response[j]['sells']['unit_price']
            sell_quantity = response[j]['sells']['quantity'] # This is the quantity for the top offer

            prices[id] = {'buy_price': buy_price, 'sell_price': sell_price, 'buy_quantity': buy_quantity, 'sell_quantity': sell_quantity}


    return prices

def getListings():
    page_count = 1
    listings = {}
    page_counter = 0

    while(page_counter < page_count):
        print("New page " + str(page_counter))
        count_string = str(page_counter)
        try:
            res = requests.get('https://api.guildwars2.com/v2/commerce/listings?page='+count_string+'&page_size=200')
            response = json.loads(res.text)
        except:
            print(count_string)
            print(res.status_code)
            print(res.text)
            page_counter += 1
            continue

        if(page_counter == 0):
            page_count = int(res.headers['X-Page-Total'])
            print(page_count)

        for j in range(int(res.headers['X-Result-Count'])):
            id = response[j]['id']
            buy_listings = {}
            sell_listings = {}
            for item in response[j]['buys']:
                buy_listings[item['unit_price']] = item['quantity']
            for item in response[j]['sells']:
                sell_listings[item['unit_price']] = item['quantity']
            listings[id] = {'buy_listings': buy_listings, 'sell_listings': sell_listings}

        page_counter += 1

    return listings

def calculate_supply(id, listings):
    sell_listings = listings[id]['sell_listings']
    supply = sum(sell_listings.values()) 
    return supply

def calculate_demand(id, listings):
    buy_listings = listings[id]['buy_listings']
    demand = sum(buy_listings.values())
    return demand

if __name__ == '__main__':
    current_datetime = datetime.datetime.now()
    conn = sqlite3.connect('gw2.db')
    cursor = conn.cursor()

    listings = getListings()
    for id in listings.keys():
        buy_prices = listings[id]['buy_listings'].keys()
        sell_prices = listings[id]['sell_listings'].keys()
        if (len(buy_prices) > 0):
            top_buy_price = max(buy_prices)
        else:
            continue
        if (len(sell_prices) > 0):
            top_sell_price = min(sell_prices)
        else:
            continue
        supply = calculate_supply(id, listings)
        demand = calculate_demand(id, listings)
        cursor.execute("delete from tp where ItemID=?", (id,))
        cursor.execute("insert into tp(ItemID, TopBuyPrice, TopSellPrice, Supply, Demand, LastUpdatedTime) values (?, ?, ?, ?, ?, ?)", (id, top_buy_price, top_sell_price, supply, demand, current_datetime))

    conn.commit()
    cursor.close()
    conn.close()

