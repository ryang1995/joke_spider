# -*- coding: utf-8 -*-
# @author Rui Y
# @version 2

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time, random
from multiprocessing import Pool

def get_one_page(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        print(response.status_code)
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
            articlePage = get_one_page('http://www.qiushibaike.com/article/' + str(id))
            content = parse_article_content(articlePage)
        yield {
            'name' : name,
            'content' : content
        }

def main(url):
    html = get_one_page(url)
    for joke in parse_one_page(html):
        write_to_file(joke)


if __name__ == '__main__':
    urls = []
    for i in range(1, 36):
        urls.append('https://www.qiushibaike.com/text/page/' + str(i) + '/')
    start = time.time()
    p = Pool(10)
    for url in urls:
        p.apply_async(main, args=(url, ))
        time.sleep(random.random()*3)
    p.close()
    p.join()
    end = time.time()
    time = end - start
    with open('jokeResult.txt', 'a') as f:
        f.write('Process time: ' + str(time) + ' seconds\n')
        f.close()