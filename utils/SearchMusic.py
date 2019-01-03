__author__ = "Jent Zhang"

import urllib.request
import urllib.parse
import json


def serch_handler(msg):
    """
    处理音乐搜索结果
    :param msg: 搜索信息
    :return:
    """
    # url = 'https://www.ximalaya.com/revision/search?core=all&kw={0}&spellchecker=true&device=iPhone'
    url='https://www.ximalaya.com/revision/search?kw={0}&page=1&spellchecker=false&condition=relation&rows=50&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    # 添加代理
    headers = {'User-Agent': user_agent}

    request_url = url.format(urllib.parse.quote(msg))
    # print(request_url)

    req = urllib.request.Request(request_url, None, headers)

    response = urllib.request.urlopen(req)

    the_page = response.read()

    return json.loads(the_page.decode("utf8"))


if __name__ == '__main__':
    res = serch_handler('爱的故事上集')
    print(res)
