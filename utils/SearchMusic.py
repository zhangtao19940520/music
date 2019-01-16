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
    url = 'https://www.ximalaya.com/revision/search?kw={0}&page=1&spellchecker=false&condition=relation&rows=50&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false'

    request_url = url.format(urllib.parse.quote(msg))  # url编码

    return get_url_response(request_url)


def recommend_tp():
    """
    获取推荐榜单
    :return:
    """
    url = "https://www.ximalaya.com/revision/rank/v1/album/getCategoryRankPage?code=yinyue&pageNum=1&pageSize=100&rankId=302"

    return get_url_response(url)


def album_info(albumId):
    """
    获取专辑音乐详情列表
    :param albumId:
    :return:
    """
    url = "https://www.ximalaya.com/revision/play/album?albumId={0}&pageNum=1&sort=-1&pageSize=30"
    request_url = url.format(albumId)
    return get_url_response(request_url)


def get_url_response(request_url):
    """
    获取网络返回结果
    :param request_url:请求的url
    :return:
    """
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    # 添加代理
    headers = {'User-Agent': user_agent}

    req = urllib.request.Request(request_url, None, headers)

    response = urllib.request.urlopen(req)

    the_page = response.read()

    return json.loads(the_page.decode("utf8"))


if __name__ == '__main__':
    # res = serch_handler('爱的故事上集')
    # res = recommend_tp()
    res = album_info(20276622)
    print(res)
