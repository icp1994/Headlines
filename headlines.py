import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/bbc")
def bbc():
    return get_news('bbc')


@app.route("/cnn")
def cnn():
    return get_news('cnn')


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> BBC Headlines </h1>
            <b>{}</b> <br/>
            <i>{}</i> <br/>
            <p>{}</p> <br/>
        </body>
    </html>""".format(first_article.get('title'), first_article.get(
        'published'), first_article.get('summary'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
