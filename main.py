import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

response_stock_name = requests.get(url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_NAME}&interval=15min&apikey=N0X23PUZ71KKYKS2')
response_stock_name.raise_for_status()
stock_data = response_stock_name.json()

response_stock_news = requests.get(url=f'https://newsapi.org/v2/everything?q={COMPANY_NAME}&from=2023-04-18&sortBy=popularity&apiKey=e8862c1c074e47ae883f26219180c10b')
response_stock_news.raise_for_status()
stock_news = response_stock_news.json()


current_date = date.today()
yesterday_date = current_date - timedelta(days=1)
yesterday = yesterday_date.strftime('%Y-%m-%d')


day_before_yesterday_date = current_date - timedelta(days=2)
day_before_yesterday = day_before_yesterday_date.strftime('%Y-%m-%d')

yesterdays_close = stock_data["Time Series (Daily)"][yesterday]["4. close"]
day_before_yesterdays_close = stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"]


difference = abs(float(yesterdays_close) - float(day_before_yesterdays_close))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

average = (difference / float(day_before_yesterdays_close))
percentage_difference =  round(average * 100)


if abs(percentage_difference) > 5:
    three_articles = stock_news["articles"][0:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBrief: {article['description']} \nURL: {article['url']}" for article in three_articles]

    for news in formatted_articles:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
            body=news,
            from_='+18885966435',
            to=''
        )
    print(message.status)

