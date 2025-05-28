import streamlit as st 
from pymongo import MongoClient
import requests
from datetime import datetime , date ,timezone
from math import *
import json 
import pandas as pd 
import plotly.express as px



mongo_user='mattaharimadhav2004'
mongo_pass='chQNUDwVPr0Ov5jx'
uri=f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.yzrkrnz.mongodb.net/"
client=MongoClient(uri)

db = client["crypto_coins"]
collection={
    'bitcoin': db["bitcoin"],
    'ethereum': db["ethereum"],
    'solana': db["solana"],
    'recent_fetched_at':db['recent_fetched_at']
}

coins=['bitcoin','ethereum','solana']

for coin in coins:
    time= collection['recent_fetched_at'].find_one({"name": coin})
    time=time['timestamp']
    with open("time.json", "r") as f:
        data = json.load(f)
    data[coin] = time
    with open("time.json", "w") as f:
        json.dump(data, f, indent=4)
    print(time)
    data = collection[coin].find_one({"fetched_at": time})
    print(data.get('current_price'))

def diff(fetched):
    timestamp_dt = datetime.fromisoformat(fetched)
    now_utc = datetime.now(timezone.utc)
    time_diff = now_utc - timestamp_dt
    return floor(time_diff.total_seconds() / 60)

#                                   last updated
#==========================================================================================
st.header('recently updated before')
with open("time.json", "r") as f:
    data = json.load(f)
st.write(f"bitcoin data updated:  {diff(data['bitcoin'])} mins ago")
st.write(f"ethereum data updated: {diff(data['ethereum'])} mins ago")
st.write(f"solana data updated:   {diff(data['solana'])} mins ago")

#                             fetch data from mongodb
#===========================================================================================

def fetch_data_from_mongo():
    db = client["crypto_coins"]
    collections = {
        'bitcoin': db["bitcoin"],
        'ethereum': db["ethereum"],
        'solana': db["solana"],
        'recent_fetched_at':db['recent_fetched_at']

    }
    current_lis=[0,0,0]
    coins=['bitcoin','ethereum','solana']
    for index,coin in enumerate(coins):
        
        time= collection['recent_fetched_at'].find_one({"name": coin})
        print(time)
        coin_data = collections[coin].find_one({'fetched_at':time['timestamp']})
        current_lis[index]=[
            coin_data["id"],
            coin_data["current_price"],
            coin_data["market_cap"],
            coin_data["market_cap_rank"],
            coin_data["fully_diluted_valuation"],
            coin_data["total_volume"],
            coin_data["high_24h"],
            coin_data["low_24h"],
            coin_data["price_change_24h"],
            coin_data["price_change_percentage_24h"],
            coin_data["market_cap_change_24h"],
            coin_data["market_cap_change_percentage_24h"]
        ]
        print("coin data : ",coin_data)
    return current_lis

# Initialize session state

if "current_data_lis" not in st.session_state:
    #run_on_date_change(new_timestamp)
    st.session_state.current_data_lis = []

print("current_data_lis",st.session_state.current_data_lis)
# Compare with previous timestamp

if len(st.session_state.current_data_lis) == 0:
    st.session_state.current_data_lis = fetch_data_from_mongo()
    st.write("🔄 we did fetch new data.")
else:
    st.write("✅ You didn't change the date")


#                                      Plots 
#===========================================================================================

columns = [
    "id", "current_price", "market_cap", "market_cap_rank",
    "fully_diluted_valuation", "total_volume", "high_24h", "low_24h",
    "price_change_24h", "price_change_percentage_24h",
    "market_cap_change_24h", "market_cap_change_percentage_24h"
]

# Convert to DataFrame
df = pd.DataFrame(st.session_state.current_data_lis, columns=columns)
st.dataframe(df)
# Display or use the DataFrame
# print(df)
y_axis = st.selectbox(
    "Select metric for Y-axis",
    [
        "current_price", "market_cap", "market_cap_rank",
        "fully_diluted_valuation", "total_volume", "high_24h", "low_24h",
        "price_change_24h", "price_change_percentage_24h",
        "market_cap_change_24h", "market_cap_change_percentage_24h"
    ]
)

# 📊 Create bar plot
fig = px.bar(df, x="id", y=y_axis, color="id", title=f"{y_axis} by Coin ID")
st.plotly_chart(fig)

#                                   Date Base Analytics 
#============================================================================================

st.header("Date Base Analytics")


d = st.date_input("target date", date(2024, 7, 6))
formatted_dat = d.strftime('%d-%m-%Y')
print(formatted_dat)

def run_on_date_change(dat=formatted_dat):
    op={}
    coins=['bitcoin','ethereum','solana']
    for coin in coins:
        lis=[]
        data_on_specific_date_url=f"https://api.coingecko.com/api/v3/coins/{coin}/history"
        params = {
            'date': formatted_dat,           # Required format: dd-mm-yyyy
            'localization': 'false'      
        }
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "CG-2evxkAj6hSZcfSsh82U1bV6S" 
        }
        response = requests.get(data_on_specific_date_url,headers=headers, params=params)
        print(response)
        data = response.json()
        id = data.get('id', 'n/a')
        name = data.get('name', 'n/a')
        market_data = data.get('market_data', {})
        current_price_inr = market_data.get('current_price', {}).get('inr', 'n/a')
        market_cap_inr = market_data.get('market_cap', {}).get('inr', 'n/a')
        total_volume_inr = market_data.get('total_volume', {}).get('inr', 'n/a')
        lis.append(id)
        lis.append(name)
        lis.append(current_price_inr)
        lis.append(market_cap_inr)
        lis.append(total_volume_inr)
        op[coin]=lis
    return op
new_timestamp = formatted_dat

# Initialize session state
if "last_timestamp" not in st.session_state:
    #run_on_date_change(new_timestamp)
    st.session_state.last_timestamp = None
print('new_timestamp : ',new_timestamp)
print("last_timestamp",st.session_state.last_timestamp)
# Compare with previous timestamp
if "date_based_dict" not in st.session_state:
    st.session_state.date_based_dict = {}

if new_timestamp != st.session_state.last_timestamp:
    st.session_state.date_based_dict = run_on_date_change(new_timestamp)
    st.session_state.last_timestamp = new_timestamp
    st.write("🔄 Data fetched for new date.")
else:
    st.write("✅ You didn't change the date")

# Display results
columns = ["ID", "Name", "Current Price", "Market Cap", "Total Volume"]
df = pd.DataFrame.from_dict(st.session_state.date_based_dict, orient='index', columns=columns)

st.subheader(f"📅 Data for {formatted_dat}")
st.table(df)
y_axis = st.selectbox(
    "Select metric for Y-axis",
    ["Current Price", "Market Cap", "Total Volume"]
)

# 📊 Create bar plot
fig = px.bar(df, x="ID", y=y_axis, color="ID", title=f"{y_axis} by Coin ID on {st.session_state.last_timestamp}")
st.plotly_chart(fig)
