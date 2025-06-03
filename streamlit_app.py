import streamlit as st 
from pymongo import MongoClient
import requests
from datetime import datetime , date ,timezone
from math import *
import json 
import pandas as pd 
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown(""" 
<nav class="navbar navbar-expand-lg navbar-light" style="background-color: #FF4B4B;">
  <a class="navbar-brand" href="https://github.com/Harimadhavmatta/crypto_coin_app" style="text-decoration: none;">Crypto App</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="https://github.com/Harimadhavmatta/">MY Github <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="https://www.linkedin.com/in/hari-madhav-matta-766b9b272/">Linkedin<span class="sr-only">(current)</span></a>
      </li>
    </ul>
  </div>
</nav>
""",unsafe_allow_html=True)
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
    # print(time)
    data = collection[coin].find_one({"fetched_at": time})
    # print(data.get('current_price'))

def diff(fetched):
    timestamp_dt = datetime.fromisoformat(fetched)
    now_utc = datetime.now(timezone.utc)
    time_diff = now_utc - timestamp_dt
    return floor(time_diff.total_seconds() / 60)

#                                   last updated
#==========================================================================================
st.header('Data Updation Status')
with open("time.json", "r") as f:
    data = json.load(f)
st.write(f"Bitcoin data updated:  {diff(data['bitcoin'])} mins ago")
st.write(f"Ethereum data updated: {diff(data['ethereum'])} mins ago")
st.write(f"Solana data updated:   {diff(data['solana'])} mins ago")

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
        # print(time)
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
        # print("coin data : ",coin_data)
    return current_lis





#                              Fetch Historical Data 
#===========================================================================================

def historical_data():
    historical_data_dict={}
    coins=['bitcoin','ethereum','solana']
    for coin in coins:
        docs=list(collection[coin].find().sort('_id', 1))
        historical_data_dict[coin]=docs
    return historical_data_dict
if "historical_data_dict" not in st.session_state:
    #run_on_date_change(new_timestamp)
    st.session_state.historical_data_dict = {}

# print("historical_data_dict",st.session_state.historical_data_dict)
# Compare with previous timestamp
st.subheader('Did i fetch historical data from mongodb ')
if len(st.session_state.historical_data_dict) == 0:
    st.session_state.historical_data_dict = historical_data()
    st.write("🔄 Historical Data Is Refreshed .")
else:
    st.write("✅ Historical Data From Cache Reload to refresh . ")

#                                 Historical Plots 
#===========================================================================================

st.title("Crypto Data Historical Visualization")


crypto_coin = st.selectbox(
    "Select coin",
    [
        'bitcoin',
        'ethereum',
        'solana'
    ]
)

y_axis=st.selectbox(
    "Select Y-axis",
    [
        'current_price','market_cap','market_cap_rank','fully_diluted_valuation','total_volume',
        'high_24h','low_24h','price_change_24h','price_change_percentage_24h','market_cap_change_24h',
        'market_cap_change_percentage_24h','circulating_supply','total_supply','max_supply','ath',
        'ath_change_percentage','ath_date','atl','atl_change_percentage','atl_date','roi'
    ]
)






data_lis=st.session_state.historical_data_dict[crypto_coin]
df = pd.DataFrame(data_lis)
# st.dataframe(df)

# Field classifications
line_fields = [
    'current_price', 'market_cap', 'market_cap_rank', 'fully_diluted_valuation',
    'total_volume', 'circulating_supply', 'total_supply', 'max_supply', 'ath',
    'ath_change_percentage', 'ath_date', 'atl', 'atl_change_percentage',
    'atl_date', 'roi'
]

bar_fields = [
    'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h',
    'market_cap_change_24h', 'market_cap_change_percentage_24h'
]




df = df.iloc[20:].reset_index(drop=True)


df['fetched_at'] = pd.to_datetime(df['fetched_at'], errors='coerce', utc=True)


x = df['fetched_at'].values

y=df[y_axis]
# Plot
fig, ax = plt.subplots(figsize=(12, 6))
if y_axis in line_fields:
    ax.plot(x, y, marker='o', linestyle='-')
else:
    ax.bar(x, y, color='skyblue')

# Formatting
# Beautify label for display
formatted_label = y_axis.replace("_", " ").title()

ax.set_xlabel("Date")
ax.set_ylabel(formatted_label)
ax.set_title(f"{formatted_label} vs Date")
plt.xticks(rotation=45)
plt.tight_layout()

# Display in Streamlit
st.pyplot(fig)



#                                      Plots 
#===========================================================================================

columns = [
    "id", "current_price", "market_cap", "market_cap_rank",
    "fully_diluted_valuation", "total_volume", "high_24h", "low_24h",
    "price_change_24h", "price_change_percentage_24h",
    "market_cap_change_24h", "market_cap_change_percentage_24h"
]

# Initialize session state

if "current_data_lis" not in st.session_state:
    #run_on_date_change(new_timestamp)
    st.session_state.current_data_lis = []

# print("current_data_lis",st.session_state.current_data_lis)
# Compare with previous timestamp
st.subheader('Did i fetch current data from mongodb ')
if len(st.session_state.current_data_lis) == 0:
    st.session_state.current_data_lis = fetch_data_from_mongo()
    st.write("🔄 we did fetch new data from mongodb .")
else:
    st.write("✅ This data is from cache . ")

# Convert to DataFrame
df = pd.DataFrame(st.session_state.current_data_lis, columns=columns)
st.subheader('These are the current stats of three coins . ')
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
fig = px.bar(df, x="id", y=y_axis, color="id", title=f"{y_axis} v/s Coin ID")
st.plotly_chart(fig)

#                                   Date Base Analytics 
#============================================================================================

st.header("Date Base Analytics")


d = st.date_input("Target date", date(2024, 7, 6))
formatted_dat = d.strftime('%d-%m-%Y')
# print(formatted_dat)

def run_on_date_change(dat=formatted_dat):
    op={}
    coins=['bitcoin','ethereum','solana']
    for coin in coins:
        lis=[]
        data_on_specific_date_url=f"https://api.coingecko.com/api/v3/coins/{coin}/history"
        params = {
            'date': formatted_dat,          
            'localization': 'false'      
        }
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "CG-2evxkAj6hSZcfSsh82U1bV6S" 
        }
        response = requests.get(data_on_specific_date_url,headers=headers, params=params)
        # print(response)
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
# print('new_timestamp : ',new_timestamp)
# print("last_timestamp",st.session_state.last_timestamp)
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


y_axis = st.selectbox(
    "Select metric for Y-axis",
    ["Current Price", "Market Cap", "Total Volume"]
)

# 📊 Create bar plot
fig = px.bar(df, x="ID", y=y_axis, color="ID", title=f"{y_axis} v/s Coin ID on {st.session_state.last_timestamp}")
st.plotly_chart(fig)
