# joke_spider
Requests + BeautifulSoup: Crawl text info from qiushi website

# 糗事百科段子爬虫
采用Requests + BeautifulSoup 方法爬取[糗事百科](https://www.qiushibaike.com/text/)上的段子并保存在本地文件中    

跟爬取猫眼top100电影不同的在于：  
部分长段子不会完全显示，需要点击查看全文后查看全文，因此在爬取过程中判断爬到的内容是否有 查看全文 几个字，若有获取这一段内容的id号，进入单独的界面爬取全文。

Difference with [movietop100_crawler](https://github.com/ryang1995/moveTop100_crawler):
The long joke won't be showed on the main page, you need click a button to another page to see the whole joke, so this program is going to check if there's the button in each content and get the own id, crawl the full text in the single page connected to the ID.

#### 开发环境 Dependencies
- python 3.x

#### 第三方库 Third-party Libraries
- Requests   
- BeautifulSoup

#### 得到的结果 Results
<img src="https://github.com/ryang1995/joke_spider/blob/master/results.png" alt="GitHub" title="snapshot">
