# coding: utf-8
# 17-10-5, created by tuitu
import io
import os
import re
from urllib.parse import quote

import requests
from PIL import Image
from bs4 import BeautifulSoup


def remove_emoji(text):
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
    # try:
    #     # UCS-4
    #     highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    # except re.error:
    #     # UCS-2
    #     highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    # # mytext = u'<some string containing 4-byte chars>'
    # return highpoints.sub(u'\u25FD', text)
    # from cucco import Cucco
    # cucco = Cucco()
    # return cucco.replace_emojis(text)


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
        # print(self.url())
        # agen = agent.get()
        # print(agen)
        agen = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        headers = {
            'Host': "s.weibo.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": agen,
            'referer': 'http://s.weibo.com/weibo/%25E5%2581%25B6%25E9%2581%2587%25E5%2591%25A8%25E5%2586%25AC%25E9%259B%25A8&Refer=STopic_top'
        }
        ip = requests.get("http://127.0.0.1:5010/get/").content.decode('utf-8')
        proxies = {'http': 'https://82.130.196.153:65301',
                   'https': 'https://82.130.196.153:65301'}
        # proxies = {'http': 'http://' + ip,
        #            'https': 'http://' + ip}
        print("proxies:", proxies)
        r = requests.get('https://www.baidu.com', headers=headers, proxies=proxies)
        print('success')
        return
        # 页面404
        if r.status_code is 404:
            print('404...')
            return

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

        print('success!')
        return
        # weibos = parser.find_all(mid=True)

        # for m in weibos:
        # weibo id
        # mid = m.get('mid')
        # 微博文字内容
        # message = m.find('p').text.strip()
        # 微博图片
        # imgs = m.find_all('img', attrs={'class': 'bigcursor'})
        # 微博属性: 收藏, 转发, 评论, 赞
        # mattrs = m.find('ul', attrs={'class': 'feed_action_info feed_action_row4'}).find_all('li')
        # print('mid:', mid)
        # for attr in mattrs:
        #     em = attr.find('em')
        #     if em and em.text:
        #         print(em.text.strip(), end='  ')
        #     else:
        #         print(0, end='  ')

        # print('')
        # 内容中可能带有emoji
        # print("message:", remove_emoji(message))

        # for img in imgs:
        #     print(img.get('src'))
        # print('-------------------------------')

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


if __name__ == '__main__':
    i = 0
    while True:
        crawl = Crawler(keyword="中国")
        try:
            crawl.fetch()
            print('--------------', i)

        except:
            print('error')
            print('--------------', i)
        i += 1
    # os.system("""(echo authenticate '"1965972530"'; echo signal newnym; echo \
    # quit) | nc localhost 9051""")
    # if i % 5 == 0:
    #     tor.switch_ip()
