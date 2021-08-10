import re
import requests
from bs4 import BeautifulSoup
import time
class Website:
    def __init__(self, url, targetPattern, commentTag, bodyTag, errorTags):
        self.url = url
        self.targetPattern = targetPattern
        self.commentTag = commentTag
        self.bodyTag = bodyTag
        self.errorTags = errorTags

class Content:
    def __init__(self):
        with open("comment0807.txt", mode="rt", encoding="utf-8") as f:
            self.comments = f.read().splitlines()
        with open("body0807.txt", mode="rt", encoding="utf-8") as f:
            self.body = f.read().splitlines()
    
    def printing(self):
        print(len(self.comments)-len(self.body))
        print(len(self.body))

    def setContent(self, comments, body):
        self.comments.extend([comment.replace('\n', '') for comment in comments])
        self.comments.append('[END]')
        self.body.append(body[0].replace('\n', ''))
        print(body[0].replace('\n', ''))
        print([comment.replace('\n', '') for comment in comments])
    
    def setContent1(self, comments, body):
        self.comments.extend([comment.replace('\n', '/') for comment in comments])
        self.body.extend([body[0].replace('\n', '/')])#*len(comments))
        print(body[0].replace('\n', '/'))
        #print([comment.replace('\n', '') for comment in comments])
    
    def save(self, commentPath, bodyPath):
        with open(commentPath, mode="w", encoding='utf-8') as f:
            f.write('\n'.join(self.comments))
        with open(bodyPath, mode="w", encoding='utf-8') as f:
            f.write('\n'.join(self.body))


class Crawler:
    def __init__(self, site, headers, contentObj):
        self.site = site
        with open("urlCash0807.txt", mode="rt", encoding="utf-8") as f:
            self.visited = f.read().splitlines()
        self.headers = headers
        self.content = contentObj

    def getPage(self, url):
        try:
            req = requests.get(url=url, headers = self.headers, proxies=proxies)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        num=0
        selectedElems = pageObj.select(selector)
        elems = []
        if selectedElems is not None and len(selectedElems) > 0:
            for elem in selectedElems:
                if(len(elem.get_text())>15):
                    #return [elem.get_text()]
                    elems.append(elem.get_text())
            #return [elem.get_text() for elem in selectedElems]
            if len(elem)>0:
                return elems
        return None

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            if bs.find('a', href=re.compile(self.site.targetPattern)) is not None:
                impressionPage = bs.find('a', href=re.compile(self.site.targetPattern)).attrs['href']
                bsi = self.getPage(impressionPage)
                comments = self.safeGet(bsi, self.site.commentTag)
                body = self.safeGet(bs, self.site.bodyTag)
                # if comments != None and body != None:
                self.content.setContent1(comments, body)
        
    def crawl(self):
        # if self.site.url not in self.visited:
        #     self.visited.append(self.site.url)
        #     with open("urlCash.txt", mode="w", encoding='utf-8') as f:
        #         f.write('\n'.join(self.visited))
        # else:return
        i = 1
        bs = self.getPage(self.site.url)
        if bs is None:
            print("bs is None!")
            return
        if bs.find('a', href=re.compile(self.site.targetPattern)) is None:
            print("impression page is none!")
            return
        impressionPage = bs.find('a', href=re.compile(self.site.targetPattern)).attrs['href']
        bsi = self.getPage(impressionPage)
        if bsi is None:
            print("bsi is None!")
            return
        # if bsi.select_one('div.nothing') is not None:
        #     print("impression does not exist!")
        #     return
        while True:
            targetPage = "{}{}".format(self.site.url, i)
            bs = self.getPage(targetPage)
            if bs is None:
                print("bs is None!")
                break
            if bs.html is None:
                print("html is None!")
                break
            if bs.html.head.title.text =="エラー":
                print("break!!")
                break
            # if bs.select_one(self.site.errorTags[0]).select_one(self.site.errorTags[1]) is not None:
            #     break
            self.parse(targetPage)
            self.content.save("comment0807.txt", "body0807.txt")
            time.sleep(1)
            i += 1
        
def searchRankingUrls(url, headers):
    rankingList = []
    req = requests.get(url=url, headers = headers, proxies=proxies)
    bs = BeautifulSoup(req.text, "html.parser")
    box = bs.select_one('div.ranking_inbox')
    lists = box.select('div.ranking_list')
    for l in lists:
        url = l.select_one('div.rank_h').select_one('a').attrs['href']
        rankingList.append(url)
    return rankingList

def searchSearchUrls(url, headers):
    i=1
    searchList = []
    while i<=100:
        targetPage = "{}{}".format(url, i)
        if targetPage in searchList:continue
        req = requests.get(url=url, headers = headers, proxies=proxies)
        bs = BeautifulSoup(req.text, "html.parser")
        box = bs.select_one('div.l-container')
        lists = box.select('div.searchkekka_box')
        for l in lists:
            targetUrl = l.select_one('div.novel_h').select_one('a').attrs['href']
            searchList.append(targetUrl)
        print(len(searchList))
        i+=1
    print(len(searchList))
    return searchList
def scraping(urls, content):
    for url in urls:
        print(url)
        naros = Website(url, targetPattern, commentTag, bodyTag, errorTags)
        crawler = Crawler(naros, headers, content)
        crawler.crawl()



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"} #ユーザエージェント設定
proxies = {
    "http":"http://proxy.uec.ac.jp:8080",
    "https":"http://proxy.uec.ac.jp:8080",
}
targetPattern = '..\/impression\/list\/..'
commentTag = "div.waku > div.comment"
bodyTag = "#novel_honbun"
rankingUrl = "https://yomou.syosetu.com/rank/list/type/monthly_total/"
rankingUrl2 = "https://yomou.syosetu.com/rank/list/type/daily_total/"
rankingUrl3 = "https://yomou.syosetu.com/rank/list/type/weekly_total/"
rankingUrl4 = "https://yomou.syosetu.com/rank/list/type/quarter_total/"
rankingUrl5 = "https://yomou.syosetu.com/rank/list/type/yearly_total/"
rankingUrl6 = "https://yomou.syosetu.com/rank/list/type/total_total/"
searchUrl = "https://yomou.syosetu.com/search/search/?&order_former=search&order=new&notnizi=1&p="
searchUrl2 = "https://yomou.syosetu.com/search.php?&order_former=search&order=favnovelcnt&notnizi=1&p="
searchUrl3 = "https://yomou.syosetu.com/search.php?&order_former=search&order=weeklypoint&notnizi=1&p="
errorTags = ["#container", "#contents_main"]
#urls = searchSearchUrls(searchUrl2, headers)
#urls.extend(searchSearchUrls(searchUrl, headers))
#urls.extend(searchSearchUrls(searchUrl3, headers))
#urls = searchRankingUrls(rankingUrl, headers)
#urls.extend(searchRankingUrls(rankingUrl3, headers))
#urls.extend(searchRankingUrls(rankingUrl4, headers))
#urls.extend(searchRankingUrls(rankingUrl5, headers))
#urls.extend(searchRankingUrls(rankingUrl6, headers))
#print(len(urls))
urls = ["https://ncode.syosetu.com/n1383gq/","https://ncode.syosetu.com/n2152gq/","https://ncode.syosetu.com/n1563gr/","https://ncode.syosetu.com/n6876gq/","https://ncode.syosetu.com/n1833gr/","https://ncode.syosetu.com/n5285gp/"]
content = Content()
scraping(urls, content)
content.printing()
content.save("comment0807.txt", "body0807.txt")






