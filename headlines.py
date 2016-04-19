import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route("/")
def get_news():
    feed = feedparser.parse(BBC_FEED)
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
