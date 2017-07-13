# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def get_article_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_article_content(article):
    # Get content
    content = BeautifulSoup(article, 'html.parser').find('div', {'class':'content'}).text.strip()
    return content

def write_to_file(article):
    with open('jokeResult.txt', 'a', encoding='utf-8') as f:
        f.write('User: ' + article['name'] + '\n')
        f.write(article['content']+'\n\n')
        f.close()

def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    joke_data = soup.find_all('div', {'class': 'article block untagged mb15'})
    for item in joke_data:
        # Get User Name
        name = item.find('div', {'class': 'author clearfix'}).find('h2').text.strip()
        # Get joke content
        content = item.find('div', {'class': 'content'}).text.strip()
        # if joke is too long then get to another page to get the whole content
        if '查看全文' in content:
            # Get content-id, then can get url
            id = item['id'].replace('qiushi_tag_', '')
            articlePage = get_article_page('http://www.qiushibaike.com/article/' + str(id))
            content = parse_article_content(articlePage)
        yield {
            'name' : name,
            'content' : content
        }

def main(page):
    url = 'https://www.qiushibaike.com/text/page/' + str(page+1)
    html = get_one_page(url)
    for joke in parse_one_page(html):
        write_to_file(joke)

if __name__ == '__main__':
    start = time.time()
    for i in range(35):
        main(i)
    end = time.time()
    time = end - start
    with open('jokeResult.txt', 'a') as f:
        f.write('Process time: ' + str(time) + ' seconds\n')
        f.close()