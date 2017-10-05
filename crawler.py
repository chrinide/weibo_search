# coding: utf-8
# 17-10-5, created by tuitu
import io
import requests
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image,ImageEnhance

def remove_emoji(text):
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


class Crawler:
    def __init__(self, keyword, mtype=0, sub='suball',
                 timescope=None, region=None, page=1, refer='g'):
        self.api = 'http://s.weibo.com/weibo/'
        self.params = {
            'keyword': keyword,
            'mtype': mtype,
            'sub': sub,
            'timescope': timescope,
            'region': region,
            'page': page,
            'refer': refer
        }

    def url(self):
        # 逐个参数处理

        # keyword 两次编码
        keyword = quote(quote(self.params['keyword']))

        # type, 类型
        # 共有6种
        # 全部: typeall=1, 热门: xsort=hot, 原创: scope=ori
        # 关注人: atten=1, 认证用户: vip=1, 媒体: category=4
        # type参数值为0..5, 作为元组的下标
        types = ('typeall=1', 'xsort=hot', 'scope=ori',
                 'atten=1', 'vip=1', 'category=4')
        mtype = types[self.params['mtype']]

        # sub, 包含
        # 共有五种
        # 全部: suball=1, 含图片: haspic=1,
        # 含视频: hasvideo=1, 含音乐: hasmusic=1, 含短链: haslink=1
        # sub参数值为包含名称
        sub = self.params['sub'] + '=1'

        # timescope, 时间范围
        # 参数格式如下 2017-10-04:2017-10-05
        timescope = ''
        if self.params['timescope']:
            timescope = 'timescope=custom:' + self.params['timescope']

        # region, 地区
        # 地区参数过于复杂,暂不提供
        region = ''

        # page, 页数
        page = 'page=' + str(self.params['page'])

        # refer, 来源
        refer = 'Refer=' + self.params['refer']

        link = self.api + keyword \
               + '&' + mtype \
               + '&' + sub \
               + '&' + timescope \
               + '&' + region \
               + '&' + page \
               + '&' + refer

        return link

    def fetch(self):
        print(self.url())
        # headers = {
        #     'Host':"map.baidu.com",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Connection": "keep-alive",
        #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
        # }
        # requests.session().cookies.clear()
        r = requests.get(self.url())
        print("r.status:", r.status_code)
        # print(r.content.decode('unicode_escape'))
        extractor = BeautifulSoup(r.content, 'html.parser')
        scripts = extractor.find_all('script')
        # i = 0
        # for s in scripts:
        #     print('--------------------------', i)
        #     i += 1
        #     print(s.text.encode("utf-8").decode('unicode_escape'))

        # html = self.extract_html_from_script(scripts[10].text)
        # print("html:", html)
        # self.verify(html)
        if len(scripts) < 22:
            print('Be caught...')
            return

        html = self.extract_html_from_script(scripts[21].text)
        
        parser = BeautifulSoup(html, 'html.parser')

        if parser.find('div', attrs={'class': 'search_noresult'}):
            print('No results found...')
            return

        weibos = parser.find_all(mid=True)

        for m in weibos:
            mid = m.get('mid')
            message = m.find('p').text.strip()
            imgs = m.find_all('img', attrs={'class': 'bigcursor'})

            print('mid:', mid)
            # 内容中可能带有emoji
            print("message:", remove_emoji(message))

            for img in imgs:
                print(img.get('src'))
            print('-------------------------------')

    def extract_html_from_script(self, script):
        n = script.find('html":"')
        if n is -1:
            return None
        html = script[n + 7: -12].encode("utf-8").decode('unicode_escape').replace("\\", "")
        return html

    def verify(self, script):
        # 需要验证码
        # 新浪微博验证码太变态, 放弃, 转反反爬虫
        parser = BeautifulSoup(script, 'html.parser')
        img = parser.find('img')
        print('src:', img.get('src'))
        src = 'http://s.weibo.com/weibo' + img.get('src')
        raw_img = requests.get(src).content
        data_stream = io.BytesIO(raw_img)
        image = Image.open(data_stream)
        image.show()


# while True:
crawl = Crawler(keyword="中国", timescope='2017-10-1:2017-10-5')
crawl.fetch()
