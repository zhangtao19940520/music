from django.shortcuts import render
from django.http.response import JsonResponse
from utils.SearchMusic import *


# Create your views here.
def home(request):
    """
    推荐
    :param request:
    :return:
    """
    return render(request, 'home.html')


def get_home_data(request):
    """
    获取首页加载时的相应数据
    :return:
    """
    ret = {}
    # 搜索历史
    search_history = request.COOKIES.get('search_history', '')
    if search_history:
        search_history = json.loads(search_history)
    ret['search_history'] = search_history

    # 推荐歌曲
    recommend_music_list = []  # 推荐歌单

    recommend_music_json = recommend_tp()  # 获取推荐歌单的返回结果

    recommend_music_list = recommend_music_json['data']['albums']  # 截取需要的数据

    ret['recommend_music_list'] = recommend_music_list

    return JsonResponse(ret)


def get_search_result(request):
    """
    返回搜索结果
    :param request:
    :return:
    """
    # 返回结果
    request_get = request.GET
    # 搜索的内容
    search_msg = request_get.get('search_msgs', '')
    # 获取搜索历史
    search_history_list = []
    search_history = request.COOKIES.get('search_history', '')
    if search_history:
        search_history = json.loads(search_history)
        search_history_list = search_history.split(',')
    # 搜索的结果
    search_res = serch_handler(search_msg)

    if search_res['ret'] == 200:
        if search_msg:
            if search_msg not in search_history_list:
                search_history_list.append(search_msg)
            else:
                '''
                如果搜索记录已存在，则先删除再放入到最后（JS中会将这个搜索记录倒序排列，所以此处不作处理）
                '''
                search_history_list.remove(search_msg)
                search_history_list.append(search_msg)
        return_data = {'code': '200', 'msg': search_res['msg'], 'data': search_res['data']}
    else:
        return_data = {'code': '000', 'msg': '很抱歉，没有搜到您要的结果。'}

    # 返回数据
    retResponse = JsonResponse(return_data)
    # 将搜索记录添加到搜索历史中
    retResponse.set_cookie('search_history', json.dumps(','.join(search_history_list)))

    return retResponse


def get_album_info(request, albumId):
    """
    推荐歌单详情
    :param request:
    :return:
    """
    ret = {}
    if len(albumId) > 0:
        album_info_json = album_info(albumId)
        album_info_list = album_info_json['data']['tracksAudioPlay']
        ret['album_info_list'] = album_info_list
    return JsonResponse(ret)
