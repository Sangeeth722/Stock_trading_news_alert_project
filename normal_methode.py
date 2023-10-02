STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
import requests
from telgram_message import Telegram
import os
from dotenv import load_dotenv
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


load_dotenv("c:/Users/sangeeth/PycharmProjects/EnvironmentVariables/.env.txt")


api_key = os.getenv("api_key_stock")
news_api_key = os.getenv("news_api_key")
bot_token_telegram = os.getenv("bot_token_telegram")
bot_chatId_telegram = os.getenv("bot_chatId_telegram")

parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey" :api_key
}
parameters_news = {
    "q":COMPANY_NAME,
    "apiKey":news_api_key
}


response = requests.get("https://www.alphavantage.co/query",params=parameters)
response.raise_for_status()
data = response.json()
daily_time = data["Time Series (Daily)"]
list_dic = [value for (key,value) in daily_time.items()]
#yestarday = list_dic[0]
#previous_day = list_dic[1]
#
#yestarday_stock_prize = float(daily_time[yestarday]["4. close"])
#previous_day_stock_prize = float(daily_time[previous_day]["4. close"])

yestarday_closing_stock = float(list_dic[0]["4. close"])
previous_day_closing_price = float(list_dic[1]["4. close"])

diffrence = previous_day_closing_price - yestarday_closing_stock
up_down = None
if diffrence>0:
    up_down = "⬆📈"
else:
    up_down = "🔻🔽"

percentage = round((abs(diffrence) / yestarday_closing_stock) * 100, 2)





#telegram message
telegram = Telegram(bot_token_telegram,bot_chatId_telegram)

if percentage >0:

    news_response = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
    news_response.raise_for_status()
    data_news = news_response.json()
    news_3_articles = data_news["articles"][:3]


    formated = [f" {up_down}{percentage}% title : {value['title']}\n Brief:{value['description']} " for value in news_3_articles]

    for message in formated:
        telegram.send_message(message)
print("message send succesfully")

