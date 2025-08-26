from flask import Flask, jsonify
from vnstock import Screener

app = Flask(__name__)
screener = Screener()

# Lấy toàn bộ cổ phiếu HOSE/HNX/UPCOM một lần
screener_df = screener.stock(params={"exchangeName": "HOSE,HNX,UPCOM"}, limit=1700)

@app.route("/api/stock/<symbol>")
def get_stock(symbol):
    try:
        row = screener_df[screener_df['ticker'] == symbol.upper()]
        if row.empty:
            return jsonify({"error": "Symbol not found"})

        latest_price = row.iloc[0]["price_near_realtime"]
        change_pct = row.iloc[0]["prev_1d_growth_pct"]
        change_amount = latest_price * (change_pct / 100) if latest_price and change_pct else 0  # Calculate absolute change
        volume = row.iloc[0]["avg_trading_value_5d"]
        update_time = "26/08/2025 09:25"  # Static for now; adjust if real-time data is available

        data = {
            "symbol": symbol.upper(),
            "price": float(latest_price) if latest_price else 0,
            "change_amount": float(change_amount) if change_amount else 0,
            "change_pct": float(change_pct) if change_pct else 0,
            "volume": float(volume) if volume else 0,
            "update_time": update_time
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)