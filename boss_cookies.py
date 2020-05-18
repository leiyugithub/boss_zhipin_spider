import random
from urllib import parse

import execjs
import requests


class BossCookieSpider:

    def __init__(self):
        self.js = execjs.compile(open("boss.js", "r").read())

    def main(self):
        headers = {
            "user-agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/{random.randint(1, 999)}.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }
        url = f"https://www.zhipin.com/job_detail/"
        response = requests.get(url, headers=headers)
        self.cookies_generate(response)

    def cookies_generate(self, response):
        query_str = parse.urlparse(response.url).query
        query_dict = {i.split("=")[0]: i.split("=")[1] for i in query_str.split("&")}
        seed = parse.unquote(query_dict.get("seed"))
        ts = query_dict.get("ts")
        code = self.js.call("encryption", seed, ts)
        code = parse.quote(code).replace("/", "%2F")
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "cookie": f"__zp_stoken__={code};"
        }
        url = "https://www.zhipin.com/c100010000-p100103/?page=3&ka=page-3"
        response = requests.get(url, headers=headers)
        print(response.text)
        pass


if __name__ == '__main__':
    boss_zhipin_cookie = BossCookieSpider()
    boss_zhipin_cookie.main()
