import os
from pymongo import MongoClient
import requests
from pprint import pprint

def get_dashboard_data(address):
    endpoint = "https://api.ethermine.org"
    path = f"/miner/:{address}/dashboard"

    r = None

    try:
        r = requests.get(endpoint + path)
    except Exception as e:
        print(f"Failed to get data for {address} - {e}")

    return r.json()

def store_dashboard_data(collection, address, data):
    try:
        collection.insert_one(data)
    except Exception as e:
        print(f"Failed to store data for {address} - {e}")

print("Start")

MONGO_URL = os.environ['MONGO_URL']
DB_TIER = os.environ['DB_TIER']
client = MongoClient(MONGO_URL)
db = client[DB_TIER]

addresses = db.addresses
mining_stats = db.mining_stats

for address in addresses.find():
    data = get_dashboard_data(address['address'])

    if data['status'] == 'OK':
        store_dashboard_data(mining_stats, address, data)
        print(f"Successfuly stored data for {address}!")
    else:
        print(f"Failed to get data for {address} - {data['status']}")


print("Complete")