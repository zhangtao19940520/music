from django.shortcuts import render
from django.http.response import JsonResponse
from utils.SearchMusic import *


# Create your views here.
def home(request):
    """
    排行榜
    :param request:
    :return:
    """
    return render(request, 'home.html')


def collect(request):
    """
    歌单
    :param request:
    :return:
    """
    return render(request, 'collect.html')


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    return render(request, 'home.html')


def get_search_result(request):
    """
    返回搜索结果
    :param request:
    :return:
    """
    # 返回结果
    request_get = request.GET
    search_msg = request_get.get('search_msgs', '')

    search_res = serch_handler(search_msg)

    if search_res['ret'] == 200:
        return_data = {'code': '200', 'msg': search_res['msg'], 'data': search_res['data']}
    else:
        return_data = {'code': '000', 'msg': '很抱歉，没有搜到您要的结果。'}

    # 返回数据
    retResponse = JsonResponse(return_data)

    return retResponse
