from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        hist.reset_index(inplace=True)
        
        # Convert 'Date' to datetime
        hist['Date'] = pd.to_datetime(hist['Date'])
        
        # Format 'Date' as needed
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        
        data = hist[['Date', 'Open', 'High', 'Low', 'Close']].to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

