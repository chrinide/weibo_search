# coding: utf-8
# 17-10-5, created by tuitu

import requests
from bs4 import BeautifulSoup



url = 'http://s.weibo.com/weibo/%25E5%25BC%25A0%25E7%25BB%25A7%25E7%25A7%2591%2520%25E4%25B8%258B%25E5%258E%25A8&typeall=1&suball=1&Refer=g'
r = requests.get(url)

print(r)

soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
dl = soup.find_all('script')[21]
# i = 0
# for s in dl:
#     print('------------------', i)
#     print("s:", s)
#     i += 1

n = dl.text.find('html":"')
j = dl.text[n + 7: -12].encode("utf-8").decode('unicode_escape').replace("\\", "")
soup = BeautifulSoup(j, 'html.parser')
j = soup.find_all(mid=True)
# print("dl:", j)
print(len(j))
for m in j:
    print(m.get('mid'))

x = 6
print(j[x].find('p').text)

img = j[x].find_all('img', attrs={'class': 'bigcursor'})
# img.pop(0)
if img:
    for i in img:
        print("i.get('src'):", i.get('src'))


http://s.weibo.com/weibo/%25E5%25B0%2591%25E4%25BA%2586%25E4%25B8%25AD%25E5%259B%25BD%25E6%25B8%25B8%25E5%25AE%25A2%25E7%259A%2584%25E9%25A6%2596%25E5%25B0%2594&Refer=STopic_top