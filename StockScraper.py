from bs4 import BeautifulSoup
import requests
url = "https://stockanalysis.com/markets/"
gainers_or_losers = (
    input("This application is a stock tracker, that returns the top 20 gainers or losers based on the time frame specified. Do you want to "
      "see gainers or losers: "))
if gainers_or_losers == "gainers":
    url += "gainers/"
else:
    if gainers_or_losers == "losers":
        url += "losers/"
        print('losers')
    else:
        print("INVALID INPUT" + "\n"
              "Valid inputs are \"gainers\" or \"losers\"")
        quit()

timeFrame = input("What time frame do you want your stocks in? Valid inputs are \"today\", \"week\", \"month\", \"ytd\", \"year\", \"3 years\", \"5 years\": ")
if timeFrame == "today" or timeFrame == "week" or timeFrame == "month" or timeFrame == "ytd" or timeFrame == "year" or timeFrame == "3 years" or timeFrame == "5 years":
    if timeFrame == "week":
        url += "week/"
    if timeFrame == "month":
        url+= "month/"
    if timeFrame == "ytd":
        url += "ytd/"
    if timeFrame == "year":
        url += "year/"
    if timeFrame == "3 years":
        url += "3y/"
    if timeFrame == "5 years":
        url += "5y/"
else:
    print("INVALID INPUT"
          "Valid inputs are \"today\", \"week\", \"month\", \"ytd\", \"year\", \"3 years\", \"5 years\"")
    quit()


html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')
information = soup.findAll('td', class_ = 'svelte-eurwtr')
stockDatabase = []

class Stock:
    def __init__(self, name, percentChange, price, volume, marketCap):
        self.name = name
        self.percentChange = percentChange
        self.price = price
        self.volume = volume
        self.marketCap = marketCap

    def get_name(self):
        return self.name
    def get_percentChange(self):
        return self.percentChange
    def get_price(self):
        return self.price
    def get_volume(self):
        return self.volume
    def get_marketCap(self):
        return self.marketCap


for i in range(0, 20):
    ticker = information[1 + i * 7].text
    name = information[2 + i*7].text
    percentChange = float(information[3 + i * 7].text[0:-1].replace(",", ""))
    price = float(information[4 + i*7].text.replace(",", ""))
    volume = int(information[5 + i*7].text.replace(",", ""))
    marketCap = information[6 + i*7].text
    marketCapLetter = (marketCap[-1])
    if marketCapLetter == "M":
        marketCapFinal = int(float(marketCap[0:-1]) * 1000000)
    if marketCapLetter == "B":
        marketCapFinal = int(float(marketCap[0:-1].replace(",", "")) * 1000000000)



    ticker = Stock(name, percentChange, price, volume, marketCapFinal)
    stockDatabase.append(ticker)

ordering = input("Would you like to order the stocks by percent change (most common option), price, volume, or market cap? Valid inputs are \"percent change\", \"price\", \"volume\", \"market cap\": ")
# sort by attribute, finish and publish to github
x = ""
if(ordering == "percent change"):
    sortedStocks = sorted(stockDatabase, key=lambda stock: stock.percentChange, reverse=True)
if(ordering == "price"):
    sortedStocks = sorted(stockDatabase, key=lambda stock: stock.price, reverse=True)
if(ordering == "volume"):
    sortedStocks = sorted(stockDatabase, key=lambda stock: stock.volume, reverse=True)
if(ordering == "market cap"):
    sortedStocks = sorted(stockDatabase, key=lambda stock: stock.marketCap, reverse=True)

print("Company Name, Percent Change, Price, Volume, Market Cap")

for stock in sortedStocks:
    information = stock.get_name() + ", " + str(stock.get_percentChange()) + "%, " + str(stock.get_price()) + ", " + str(stock.get_volume()) + ", " + str(stock.get_marketCap())
    print(information)

if(gainers_or_losers == "gainers"):
    for stock in sortedStocks:
        information = stock.get_name() + ", " + str(stock.get_percentChange()) + "%, " + str(
            stock.get_price()) + ", " + str(stock.get_volume()) + ", " + str(stock.get_marketCap())
        print(information)
if(gainers_or_losers == "losers"):
    for stock in sortedStocks:
        information = stock.get_name() + ", -" + str(stock.get_percentChange()) + "%, " + str(
            stock.get_price()) + ", " + str(stock.get_volume()) + ", " + str(stock.get_marketCap())
        print(information)
