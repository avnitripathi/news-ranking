import json

from bs4 import BeautifulSoup
import requests

min = 36969
def extract_headlines(website, tag, class_):
    min_news = 18
    r1 = requests.get(website)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coverpage_news = soup1.find_all(tag, class_=class_)
    news2 = [n.get_text().replace('\n', '') for n in coverpage_news]
    news = []
    for i in range(0, min_news):
        news.append(news2[i])
    print(website)
    print(len(news))
    print(len(news2))
    return list(news)

def extract_all():
    web_info = {
        "https://www.bbc.com/news/politics": {
            "tag": "span",
            "class_": "lx-stream-post__header-text gs-u-align-middle"
        },
        "https://www.theguardian.com/politics": {
            "tag": "a",
            "class_": "u-faux-block-link__overlay js-headline-text"
        },
        "https://www.dailymail.co.uk/news/uk-politics/index.html": {
            "tag": "h2",
            "class_": "linkro-darkred"
        },
        "https://www.telegraph.co.uk/politics/": {
            "tag": "a",
            "class_": "list-headline__link u-clickable-area__link"
        },
        "https://www.mirror.co.uk/news/politics/": {
            "tag": "a",
            "class_": "headline"
        },
        "https://www.express.co.uk/news/politics": {
            "tag": "h4",
            "class_": ""
        },
        "https://metro.co.uk/tag/politics/": {
            "tag": "h3", #only produces 7, use 'a' and "" for more but with ads.
            "class_": "nf-title"
        },
        "https://www.standard.co.uk/news/politics": {
            "tag": "div",
            "class_": "headline color-news_blue"
        },
        "https://www.manchestereveningnews.co.uk/all-about/politics": {
            "tag": "a",
            "class_": "headline"
        },
        "https://uk.news.yahoo.com/tagged/politics/": {
            "tag": "h3",
            "class_": "Mb(5px)"
        },
        "https://news.sky.com/politics": {
            "tag": "span",
            "class_": "sdc-site-tile__headline-text"
        },
        "https://www.thetimes.co.uk/politics": {
            "tag": "div",
            "class_": "css-x1m2h7"
        },
    }
    all_data = {}
    for k in web_info.keys():
        all_data[k] = extract_headlines(k, web_info[k]["tag"], web_info[k]["class_"])
    with open('extracted_headlines.json', 'w') as f:
        json.dump(all_data, f, indent=4)


extract_all()