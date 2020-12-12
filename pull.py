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
        msg = f"Failed to get data for {address} - {e}"
        print(msg)
        logs.insert_one({'msg': msg})

    return r.json()

def store_dashboard_data(collection, address, data):
    try:
        id = collection.insert_one(data).inserted_id
        msg = f"Wrote data for {id}"
        print(msg)
        logs.insert_one({'msg': msg})

    except Exception as e:
        msg = f"Failed to store data for {address} - {e}"
        print(msg)
        logs.insert_one({'msg': msg})

print("Start")

MONGO_URL = os.environ['MONGO_URL']
DB_TIER = os.environ['DB_TIER']
client = MongoClient(MONGO_URL)
db = client[DB_TIER]

addresses = db.addresses
mining_stats = db.mining_stats
logs = db.logs

msg = f"Connected to {MONGO_URL} in {DB_TIER}"
print(msg)
logs.insert_one({'msg': msg})

for address in addresses.find():
    data = get_dashboard_data(address['address'])

    if data['status'] == 'OK':
        store_dashboard_data(mining_stats, address, data)
        msg = f"Successfuly stored data for {address['address']}!"
        print(msg)
        logs.insert_one({'msg': msg})
    else:
        msg = f"Failed to get data for {address} - {data['status']}"
        print(msg)
        logs.insert_one({'msg': msg})

print("Complete")