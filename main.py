import requests, json, re

from flask import Flask, Response  
from flask import request as flask_request
from flask_sslify import SSLify

from tokens import api_key, bot_key
  
app = Flask(__name__)
ssl_instance = SSLify(app)

@app.route('/', methods = ['POST', 'GET'])
def index():
    #if request post then get coin data
    if flask_request.method == 'POST':
        msg = flask_request.get_json()
        #write_json(msg, 'message')
        chat_id, symbol = parse_message(msg)
        if not symbol: #if symbol is null, return something
            send_message(chat_id, 'Sike thats the wrong number')
            return Response('Ok', status = 200)
        price = get_crypto_info(symbol.upper())
        send_message(chat_id,price)
        return Response('OK', status=200), symbol
    else:
        return "<h1> CoinMarketCap Bot </h1>"
    
def parse_message(message):
    """ extract chay_id and text from incoming message """
    chat_id = message["message"]["chat"]["id"]
    coin = message["message"]["text"]
    pattern = r'/[a-z A-Z]{2,4}'
    valid = re.findall(pattern, coin)
    if valid:
        symbol = valid[0]
    else:
        symbol = ''
    return chat_id, symbol.strip('/')


def send_message(chat_id, message):
    """ reply to user"""
    url = f"https://api.telegram.org/bot{bot_key}/sendMessage"
    payload = {
        "chat_id":chat_id,
        "text": message
    }
    r = requests.post(url, json = payload)
    return r 

def write_json(data, filename = 'newfile.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent= 4, ensure_ascii= False) 


def get_crypto_info(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        
        'symbol':crypto,
        'convert':'INR'
    }
    headers = {

        'X-CMC_PRO_API_KEY':api_key
    }
    req = requests.get(url, headers = headers, params= parameters).json()
    price = req["data"][crypto]["quote"]["INR"]["price"]
    volume_24h = req["data"][crypto]["quote"]["INR"]["volume_24h"]
    market_cap = req["data"][crypto]["quote"]["INR"]["market_cap"]

    return price



def main():
    
    r = get_crypto_info('BTC')
    


    
if __name__ == "__main__":
    #main()
    app.run(debug= True)
     