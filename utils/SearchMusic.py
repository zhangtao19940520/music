__author__ = "Jent Zhang"

from urllib import parse
from urllib import request
import json
from bs4 import BeautifulSoup
import requests
import random
import re

music_url = "https://www.ximalaya.com"


def serch_handler(msg):
    """
    处理音乐搜索结果
    :param msg: 搜索信息
    :return:
    """
    # url = 'https://www.ximalaya.com/revision/search?core=all&kw={0}&spellchecker=true&device=iPhone'
    url = 'https://www.ximalaya.com/revision/search?kw={0}&page=1&spellchecker=false&condition=relation&rows=50&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false'

    request_url = url.format(parse.quote(msg))  # url编码

    return get_url_response(request_url)


def recommend_tp():
    """
    获取推荐榜单
    :return:
    """
    url = "https://www.ximalaya.com/revision/rank/v1/album/getCategoryRankPage?code=yinyue&pageNum=1&pageSize=100&rankId=302"

    return get_url_response(url)


def recommend_top():
    """
    获取推荐榜单(新方法)
    :return:
    """
    result = list()
    url = '{0}/yinyue/'.format(music_url)
    # 获取网页返回内容
    html_content = get_url_html(url)
    # 将返回的网页内容转为字符串，方便后续使用正则
    html_content = str(html_content)
    # 使用正则表达式截取需要的部分内容
    music_info = re.findall('{"albumsResult":(.*?),"urlInfo":', html_content)[0]
    # 将结果转化为json
    music_info_json = json.loads(music_info)
    # 获取音乐列表部分
    music_list = music_info_json['albums']
    # print(html_content.prettify())  # 使用prettify()格式化显示输出
    # 找到指定的div内容部分
    # html_div = html_content.find_all(name="div", attrs={"class": "content"}, limit=1)
    # for li_msg in html_div[0].find_all(name='li'):
    #     result.append({
    #         "cover_path": li_msg.find_all(name="")
    #     })
    for music_info in music_list:
        # print(music_info)
        result.append({
            "coverPath": music_info['coverPath'],
            "albumTitle": music_info['title'],
            "anchorName": music_info['anchorName'],
            "id": music_info['albumId']
        })
    return result


def album_info(albumId):
    """
    获取专辑音乐详情列表
    :param albumId:
    :return:
    """
    result = []
    url = "{0}/yinyue/{1}/".format(music_url, albumId)
    # 获取网页返回内容
    html_content = get_url_html(url)
    # 找到指定的div内容部分
    html_div = html_content.find_all(name="div", attrs={"class": "sound-list _Qp"}, limit=1)
    song_id = 0
    for li_msg in html_div[0].find_all(name='li', class_='_Vc'):
        song_href = li_msg.find_all(name='a')[0].attrs['href'],
        song_id = str(song_href[0]).split('/')[-1]
        song_info = get_song_info_by_id(song_id)
        # print(song_info)
        result.append({
            "albumName": li_msg.find_all(name='span', class_="time _Vc", limit=1)[0].string,
            "trackName": li_msg.find_all(name='span', class_="title _Vc", limit=1)[0].string,
            "trackId": song_id,
            "src": song_info['src'],
        })
    # 获取专辑信息
    song_info_list = get_song_info_list_by_album_id(song_id)
    # print(song_info_list)
    # 完善封面信息
    for res in result:
        res['trackCoverPath'] = "https://imagev2.xmcdn.com/" + \
                                [i['trackCoverPath'] for i in song_info_list if str(i['trackId']) == res['trackId']][0]
    # print(result)
    return result


def get_song_info_by_id(song_id):
    """
    通过歌曲ID获取歌曲信息
    :return:
    """
    url = "{0}/revision/play/v1/audio?id={1}&ptype=1".format(music_url, song_id)
    result = get_url_response(url)
    return result['data']


def get_song_info_list_by_album_id(song_id):
    """
    根据song_id获取所有歌曲的其他信息
    :param song_id:
    :return:
    """
    url = "{0}/revision/play/v1/show?id={1}&sort=1&size=300&ptype=1".format(music_url, song_id)
    result = get_url_response(url)
    return result['data']['tracksAudioPlay']


def get_url_response(request_url):
    """
    获取网络返回结果
    :param request_url:请求的url
    :return:
    """
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    # 添加代理
    headers = {'User-Agent': user_agent}

    req = request.Request(request_url, None, headers)

    response = request.urlopen(req)

    the_page = response.read()

    return json.loads(the_page.decode("utf8"))


def get_url_html(url):
    """
    获取页面的html内容
    :param url:
    :return:
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    response = requests.get(
        url,
        headers=header
    )
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        return ""


if __name__ == '__main__':
    # res = serch_handler('爱的故事上集')
    # res = recommend_tp()
    album_info(3595841)
    # res = get_song_info_list_by_album_id(3595841)
    # print(res)
