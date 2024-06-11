import requests
import json

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

    for page_counter in range(page_count):
        count_string = str(page_counter)
        res = requests.get('https://api.guildwars2.com/v2/commerce/listings?page='+count_string+'&page_size=200')
        response = json.loads(res.text)
        if(page_counter == 0):
            page_count = res.headers['X-Page-Total']
        for j in range(200):
            id = response[j]['id']
            buy_listings = {}
            sell_listings = {}
            for item in response[j]['buys']:
                buy_listings[item['unit_price']] = item['quantity']
            for item in response[j]['sells']:
                sell_listings[item['unit_price']] = item['quantity']
        listings[id] = {'buy_listings': buy_listings, 'sell_listings': sell_listings}
    
    return listings

def calculate_supply(id, listings):
    sell_listings = listings[id]['sell_listings']
    supply = sum(sell_listings.values()) 
    return supply

def calculate_demand(id, listings):
    buy_listings = listings[id]['buy_listings']
    demand = sum(buy_listings.values())
    return demand


