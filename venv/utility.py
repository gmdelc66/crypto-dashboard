# import modules
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class ApiUtil:
    # get coin prices based on symbols passed in
    @staticmethod
    def coin_price(coin_list):
        # build symbol list based on list of dictionaries
        symbols = ""
        for i in coin_list:
            if symbols == "":
                symbols = i["symbol"]
            else:
                symbols = symbols + "," + i["symbol"]

        # coinmarketcap API
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': symbols,
        }
        # API_KEY is from the dev account on coinmarketcap, replace the x's
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'bee5d0df-98c7-4954-8af2-8fab7a3d8935',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    # pull out relevant data from the json return
    @staticmethod
    def parse_json(dump):
        result_list = []
        for i in dump["data"]:
            for j, k in dump["data"][i].items():
                if j == "quote":
                    for l, m in k.items():
                        result_dict = {"symbol": i, "price": m["price"], "percent_change_24h": m["percent_change_24h"]}
                        result_list.append(result_dict)
        return result_list


class CoinUtil:
    # create dictionary with coins, amounts, and cost
    # it is important to note that symbols must be capitalized and match exactly what coinmarketcap shows
    @staticmethod
    def create_coin_dict():
        # Monedas que maneja BITSO
        coin_list = [
            {"symbol": "BTC", "amount": 1, "cost": 1},
            {"symbol": "ETH", "amount": 1, "cost": 1},
            {"symbol": "XRP", "amount": 1, "cost": 1},
            {"symbol": "LTC", "amount": 1, "cost": 1},
            {"symbol": "BCH", "amount": 1, "cost": 1},
            {"symbol": "TUSD", "amount": 1, "cost": 1},
            {"symbol": "MANA", "amount": 1, "cost": 1},
            {"symbol": "BAT", "amount": 1, "cost": 1},
            {"symbol": "DAI", "amount": 1, "cost": 1}
        ]
        return coin_list

    # calculate crypto value, total gain/loss percentage, and portfolio distribution
    @staticmethod
    def calc_value(coin, dump):
        new_list = []
        total_value = 0
        for i in dump:
            for j in coin:
                if i["symbol"] == j["symbol"]:
                    value = round(i["price"] * j["amount"], 2)
                    if j["cost"] != 0:
                        total_change = (value / j["cost"] - 1) * 100
                    else:
                        total_change = 0
                    new_list.append({"symbol": j["symbol"], "amount": j["amount"], "price": i["price"], "value": value,
                                     "percent_change_24h": round(i["percent_change_24h"], 2), "total_change": round(total_change, 2)})
                    total_value = total_value + value

        # calculating portfolio distribution per coin and adding it to the dictionary for said coin
        for k in new_list:
            diversity = round(k["value"] / total_value * 100, 2)
            k["diversity"] = diversity
        return new_list
