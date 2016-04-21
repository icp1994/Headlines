import datetime
import feedparser
import json
import urllib
from flask import Flask, make_response, render_template, request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

URLS = {'weather': "http://api.openweathermap.org/data/2.5/weather?"
        "q={}&units=metric&appid=c2348ba40d2239fdc0dd9c03abf01122",
        'currency': "https://openexchangerates.org/api/latest.json?"
        "app_id=f3ef23dd99ee4acba4c5dafe2a4b9b14"}

DEFAULTS = {'publication': 'bbc',
            'city': 'Kolkata, IN',
            'currency_from': 'USD',
            'currency_to': 'INR'}


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")
def home():
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    city = get_value_with_fallback('city')
    weather = get_weather(city)

    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template(
        'home.html',
        articles=articles,
        weather=weather,
        currency_from=currency_from,
        currency_to=currency_to,
        rate=rate,
        currencies=sorted(currencies)))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)
    response.set_cookie('currency_from', currency_from, expires=expires)
    response.set_cookie('currency_to', currency_to, expires=expires)

    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']


def get_weather(query):
    url_query = urllib.parse.quote(query)
    url = URLS['weather'].format(url_query)
    data = urllib.request.urlopen(url)
    encoding = data.headers.get_content_charset()
    parsed = json.loads(data.read().decode(encoding))
    weather = None
    if parsed.get('weather'):
        weather = {"description": parsed['weather'][0]['description'],
                   "temperature": parsed['main']['temp'],
                   "city": parsed['name'],
                   "country": parsed['sys']['country']}

    return weather


def get_rate(currency_from, currency_to):
    data = urllib.request.urlopen(URLS['currency'])
    encoding = data.headers.get_content_charset()
    parsed = json.loads(data.read().decode(encoding)).get('rates')
    from_rate = parsed.get(currency_from.upper())
    to_rate = parsed.get(currency_to.upper())

    return (to_rate/from_rate, parsed.keys())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
