import os
import requests
import time

# 使用tor进行代理
url = 'http://api.ipify.org?format=json'

def getip_requests(url):
    print("(+) Sending request with plain requests...")
    r = requests.get(url)
    print("(+) IP is: " + r.text.replace("\n", ""))


def getip_requesocks(url):
    print("(+) Sending request with requesocks...")
    proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    r = requests.get(url, proxies=proxies)
    print("(+) IP is: " + r.text.replace("\n", ""))


def main():
    print("Running tests...")
    getip_requests(url)
    getip_requesocks(url)
    os.system("""(echo authenticate '"1965972530"'; echo signal newnym; echo \
    quit) | nc localhost 9051""")
    time.sleep(2)
    getip_requesocks(url)


if __name__ == "__main__":
    main()