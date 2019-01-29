from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from utils.SearchMusic import *
from utils.BaseFunction import *
from utils.MailUtils import *
from django.core.cache import cache
from .models import *


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

    #登录用户帐号
    ret['user_name'] = request.session.get('user_name', '')
    #收藏
    collect_list=collect.objects.filter(user_name=request.session.get('user_name', ''))
    collect_dic = {}
    if collect_list:
        for item in collect_list.values_list():
            collect_dic[item[2]]={
                'song_id': item[2],
                'corver_pic': item[3],
                'song_src': item[4],
                'song_name': item[5],
                'album_name': item[6],
                'song_user_name': item[7],
            }

    ret['collect_list']=collect_dic

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


def get_code(request):
    """
    获取邮箱验证码
    :param request:
    :return:
    """
    res = {}
    # 收件人邮箱
    email = request.POST.get('email', '')
    # 随机验证码
    code = get_random_code(length=6)

    if not email:
        res = {'has_error': True, 'msg': '请输入邮箱'}
        return JsonResponse(res)
    # 邮件接收方
    mailto_list = [email]
    mail = SendEmail()
    sub = '你好：{0}'.format(code)
    email_msg = "<h1>{0}</h1><p>您正在登录音乐空间，唯一标识码是{0}，5分钟内有效。如非本人操作，可不予理会。</p>".format(code)
    if mail.sendTxtMail(mailto_list, sub, email_msg, is_html=True):
        res = {'has_error': False, 'msg': '验证码已发送至邮箱，5分钟内有效。'}
        cache.set(email, code, 5 * 60)
        # print(cache.get(email))
        # print(cache.has_key(email))
    else:
        res = {'has_error': True, 'msg': '邮件发送失败'}

    return JsonResponse(res)


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    res = {}
    email = request.POST.get('email', '')
    code = request.POST.get('code', '')

    if not email:
        res = {'has_error': True, 'msg': '请输入您的邮箱'}
        return JsonResponse(res)
    elif not code:
        res = {'has_error': True, 'msg': '请输入验证码'}
        return JsonResponse(res)
    if not cache.has_key(email):
        res = {'has_error': True, 'msg': '验证码已失效'}
        return JsonResponse(res)
    if cache.get(email) != code:
        res = {'has_error': True, 'msg': '验证码不正确'}
        return JsonResponse(res)

    res = {'has_error': False, 'msg': '登录成功'}
    request.session['user_name'] = email.split('@')[0]
    return JsonResponse(res)


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()

    return redirect('/')


def collect_action(request):
    """
    收藏夹的操作（添加收藏或者取消收藏）
    :param request:
    :return:
    """
    res = {}

    user_name = request.session.get('user_name', '')
    if not user_name:
        res = {'has_error': True, 'msg': '您尚未登录，无法进行收藏相关操作'}
        return JsonResponse(res)

    song_info = {
        'user_name': user_name,
        'song_id': request.POST.get('song_id', ''),
        'corver_pic': request.POST.get('corver_pic', ''),
        'song_src': request.POST.get('song_src', ''),
        'song_name': request.POST.get('song_name', ''),
        'album_name': request.POST.get('album_name', ''),
        'song_user_name': request.POST.get('song_user_name', '')
    }

    collect_model = collect.objects.filter(user_name=user_name, song_id=song_info['song_id'])

    if not collect_model:
        if collect.objects.create(**song_info):
            res = {'has_error': False, 'msg': '已收藏'}
            return JsonResponse(res)
    else:
        collect.objects.filter(user_name=user_name, song_id=song_info['song_id']).delete()
        res = {'has_error': False, 'msg': '已取消收藏'}
        return JsonResponse(res)
