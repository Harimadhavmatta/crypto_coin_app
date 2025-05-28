# 📦 crypto_coin_app 
```
⬆️ (crypto_coin_app)
```

### 📦 Project workflow
![Your paragraph text](https://github.com/user-attachments/assets/9494ba33-dcd4-499f-b21d-edf2e6d43b58)


## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://my-crypto-coin-app.streamlit.app/)

Here's a suitable **README.md** content for your Streamlit cryptocurrency dashboard project using MongoDB and the CoinGecko API:


# 📊 Crypto Coin Dashboard (Streamlit + MongoDB)

This Streamlit web app visualizes real-time and historical cryptocurrency data (Bitcoin, Ethereum, and Solana). It fetches live data from MongoDB and allows users to view stats and date-based analytics using the [CoinGecko API](https://www.coingecko.com/en/api/documentation).

## 🔧 Tech Stack

* **Frontend**: Streamlit + Bootstrap for custom navbar
* **Backend**: Python
* **Database**: MongoDB Atlas
* **External APIs**: CoinGecko API
* **Libraries Used**: `streamlit`, `pymongo`, `requests`, `pandas`, `plotly`, `datetime`, `json`, `math`

## 🚀 Features

### ✅ Real-time Coin Status

* Connects to MongoDB Atlas to fetch the **most recent cryptocurrency data**.
* Displays when the data was last updated (in minutes ago).
* Shows key statistics like:

  * Current price
  * Market cap
  * Total volume
  * Price and market cap changes (24h)

### 📅 Date-Based Analytics

* Select any date (in the past) to view historical data for Bitcoin, Ethereum, and Solana using the CoinGecko API.
* Stats displayed for selected date:

  * Current price in INR
  * Market cap
  * Total volume

### 📈 Data Visualization

* Interactive bar charts using **Plotly Express**
* Compare different metrics (e.g., current price, market cap) across coins or on historical dates

## 🖥️ Screenshots

(You can add screenshots or gifs here.)

## 📂 Folder Structure

```
📁 crypto_coin_app
│
├── 📄 app.py            # Main Streamlit app
├── 📄 time.json         # Stores timestamps of recent fetch
├── 📄 requirements.txt  # Required Python packages
└── README.md            # Project overview
```

## 🧪 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/Harimadhavmatta/crypto_coin_app.git
cd crypto_coin_app
```

2. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

> **Note**: You must have a valid MongoDB URI and API key for CoinGecko in the script.

## 🔐 Security Notice

**IMPORTANT:** Never expose your MongoDB username/password or API keys in production. Use `.env` or secret managers for sensitive credentials.

---

## 🙋‍♂️ Author

* **Hari Madhav Matta**
  [LinkedIn](https://www.linkedin.com/in/hari-madhav-matta-766b9b272/) | [GitHub](https://github.com/Harimadhavmatta/)

---

Let me know if you want to add badges, deployment steps (like Streamlit Cloud or Render), or environment variable setup instructions.

