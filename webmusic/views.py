from django.shortcuts import render
from django.http.response import JsonResponse
from utils.SearchMusic import *


# Create your views here.
def home(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'home.html')


def charts(request):
    """
    排行榜
    :param request:
    :return:
    """
    return render(request, 'charts.html')


def collect(request):
    """
    歌单
    :param request:
    :return:
    """
    return render(request, 'collect.html')


def artist(request):
    """
    歌手
    :param request:
    :return:
    """
    return render(request, 'artist.html')


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    return render(request, 'search.html')


def get_search_result(request):
    """
    返回搜索结果
    :param request:
    :return:
    """
    # 返回结果
    return_data = {}
    request_get = request.GET
    search_msg = request_get.get('search_msgs', '')

    search_res = serch_handler(search_msg)
    # print(search_res)
    if search_res['ret']==200:
        return_data = {'code': '200', 'msg': search_res['msg'],'data':search_res['data']}
    else:
        return_data = {'code': '000', 'msg': '很抱歉，没有搜到您要的结果。'}



    return JsonResponse(return_data)
