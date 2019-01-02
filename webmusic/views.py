from django.shortcuts import render


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
