import json

from bs4 import BeautifulSoup
import requests

def extract_headlines(website, tag, class_):
    r1 = requests.get(website)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coverpage_news = soup1.find_all(tag, class_=class_)

    news = set([n.get_text().replace('\n', '') for n in coverpage_news])

    print(website)
    print(len(news))

    return list(news)

def extract_all():
    web_info = {
        "https://www.bbc.com/news/politics": {
            "tag": "h3",
            "class_": "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"
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
            "tag": "span",
            "class_": "list-headline__text"
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
            "tag": "span", #only produces 7, use 'a' and "" for more but with ads.
            "class_": "colour-box"
        },
        "https://www.channel4.com/news/politics": {
            "tag": "h2",
            "class_": "heading body"
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


    }
    all_data = {}
    for k in web_info.keys():
        all_data[k] = extract_headlines(k, web_info[k]["tag"], web_info[k]["class_"])
    with open('extracted_headlines.json', 'w') as f:
        json.dump(all_data, f, indent=4)


extract_all()
