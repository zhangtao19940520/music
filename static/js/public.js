/**
 * Created by Administrator on 2019-01-02.
 */
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        user_name: '',
        search_msg: '',
        music_list: [],
        is_searched: false,//是否执行了搜索功能
        show_page: 'home',//默认显示首页
        search_history: [],//搜索历史
        recommend_music_list: [],//推荐歌单
        album_info_list: [],//专辑歌单
        collect_list: {},
    },
    methods: {
        /**
         * 移除收藏夹
         * */
        removeCollection: function (song_id) {
            var this_vue = this;
            layer.confirm('确定取消收藏？', {
                btn: ['确定', '再想想'], //按钮
                title: '取消收藏'
            }, function () {
                var load;
                $.ajax({
                    url: 'collect_action?t=' + Math.random(),
                    type: "POST",
                    data: {song_id: song_id},
                    dataType: "JSON",
                    beforesend: function () {
                        load = layer.load();
                    },
                    success: function (response) {
                        layer.close(load);
                        var icon = 1;
                        if (response.has_error) {
                            icon = 0;
                        } else {
                            delete this_vue.collect_list.song_id;
                        }
                        layer.msg(response.msg, {icon: icon});
                        setTimeout(this_vue.loadData, 1000);
                    },
                    error: function () {
                        layer.closeAll();
                        layer.msg('取消收藏出错', {icon: 2});
                    }
                });
            });
        },
        /**
         * 添加收藏夹
         * */
        addCollection: function (obj, the) {
            var this_vue = this;
            var song_info = {
                song_id: obj.id || obj.trackId,
                corver_pic: obj.cover_path || obj.trackCoverPath,
                song_src: obj.src || obj.play_path_aacv224 || obj.play_path_aacv164,
                song_name: obj.title || obj.trackName,
                album_name: obj.album_title || obj.albumName,
                song_user_name: obj.nickname || ''
            };
            var load;
            $.ajax({
                url: 'collect_action?t=' + Math.random(),
                type: "POST",
                data: song_info,
                dataType: "JSON",
                beforesend: function () {
                    load = layer.load();
                },
                success: function (response) {
                    layer.close(load);
                    var icon = 1;
                    if (response.has_error) {
                        icon = 0;
                    } else {
                        if (this_vue.collect_list[song_info.song_id] == undefined) {
                            this_vue.collect_list[song_info.song_id] = song_info;
                            $(the.target).attr('src', '/static/images/collect.png');
                        } else {
                            delete this_vue.collect_list[song_info.song_id];
                            $(the.target).attr('src', '/static/images/nocollect.png');
                        }
                    }

                    layer.msg(response.msg, {icon: icon});

                },
                error: function () {
                    layer.closeAll();
                    layer.msg('收藏出错', {icon: 2});
                }
            });
        },
        /**
         * 用户登录
         * */
        login: function () {
            var email = $('#email').val();
            var code = $('#code').val();
            var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            if (!reg.test(email)) {
                layer.msg('邮箱格式不正确', {icon: 0});
                return false;
            }
            if (code.length == 0) {
                layer.msg('请输入验证码', {icon: 0});
                return false;
            }
            var load;
            $.ajax({
                url: '/login?t=' + Math.random(),
                data: {
                    email: email,
                    code: code
                },
                type: 'POST',
                dataType: 'JSON',
                beforesend: function () {
                    load = layer.load();
                },
                success: function (response) {
                    layer.close(load);
                    var icon = 1;
                    if (response.has_error) {
                        icon = 0;
                    } else {
                        setInterval(function () {
                            location.href = '/';
                        }, 1000)
                    }
                    layer.msg(response.msg, {icon: icon});

                },
                error: function () {
                    layer.closeAll();
                    layer.msg('登录失败', {icon: 2});
                }

            });
        },
        /**
         * 获取验证码
         * */
        getCode: function () {
            if ($('#btnGetCode').hasClass('disabled')) {
                return false;
            }
            var s = 60;
            var email = $('#email').val().trim();
            var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            if (!reg.test(email)) {
                layer.msg('邮箱格式不正确', {icon: 0});
                return false;
            }

            $('#btnGetCode').val('60 s后重新获取').addClass('disabled');
            var timer = setInterval(function () {
                s--;
                $('#btnGetCode').val(s + 's 后重新获取');
                if (s <= 0) {
                    clearInterval(timer);
                    $('#btnGetCode').val('获取验证码').removeClass('disabled');
                }
            }, 1000);
            var load;
            $.ajax({
                url: '/GetCode?t=' + Math.random(),
                type: 'POST',
                data: {
                    email: email
                },
                dataType: 'JSON',
                beforeSend: function () {
                    load = layer.load(2);
                },
                success: function (response) {
                    layer.close(load);
                    var icon = 1;
                    if (response.has_error) {
                        icon = 0;
                    }
                    layer.msg(response.msg, {icon: icon});
                },
                error: function () {
                    layer.msg('获取验证码失败', {icon: 2});
                }
            });

        },
        /**
         * 显示登录页面
         * */
        showLoginPage: function () {
            var screen_width = $('#login').width() + 'px';
            var screen_height = $('#login').height() + 'px';

            $('#login').removeClass('hidden');
            layer.load(2);
            layer.open({
                type: 1,
                shade: false,
                title: false, //不显示标题
                content: $('#login'), //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                cancel: function () {
                    layer.closeAll();
                    $('#login').addClass('hidden');
                },
                area: [screen_width, screen_height], //宽高
            });
        },
        /**
         * 获取专辑详情
         * */
        click_album_desc: function (obj) {
            var this_vue = this;
            $('.album_info').removeClass('hidden');
            var screen_width = ($(window).width() - 30) + 'px';
            var screen_height = ($(window).height() - 200) + 'px';
            $.ajax({
                url: '/get_album_info/' + obj.id,
                type: 'GET',
                dataType: 'JSON',
                beforeSend: function () {
                    layer.load();
                },
                success: function (data) {
                    layer.closeAll();
                    this_vue.album_info_list = data.album_info_list;
                    layer.open({
                        type: 1,
                        shade: false,
                        title: false, //不显示标题
                        content: $('.album_info'), //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                        cancel: function () {
                            $('.album_info').addClass('hidden');
                        },
                        area: [screen_width, screen_height], //宽高
                    });
                },
                error: function (xhr, type) {
                    layer.closeAll();
                }
            });

        },
        /**
         * 页面加载时获取初始化数据
         * */
        loadData: function () {
            var this_vue = this;
            $.ajax({
                url: '/get_home_data',
                data: {},
                type: 'GET',
                dataType: 'JSON',
                beforeSend: function () {
                    layer.load();
                },
                success: function (data) {
                    layer.closeAll();
                    //用户信息
                    this_vue.user_name = data.user_name;
                    //搜索历史
                    if (data.search_history.length > 0) {
                        this_vue.search_history = data.search_history.split(',').reverse();

                    }
                    //推荐歌单
                    this_vue.recommend_music_list = data.recommend_music_list;
                    // console.log(this_vue.recommend_music_list);
                    //收藏
                    this_vue.collect_list = data.collect_list
                },
                error: function (xhr, type) {
                    layer.closeAll();
                }
            });
        },
        /**
         * 页面加载
         * */
        loadPage: function () {
            var this_vue = this;
            var navs = $('.navs a');
            navs.each(function () {
                $(this).removeClass('active');
                var data_url = $(this).attr('target-url');
                if (this_vue.show_page == data_url) {
                    $(this).addClass('active');
                }
            });
        },
        /**
         * 页面切换
         * page_name:目标页
         * */
        pageChange: function (page_name) {
            this.show_page = page_name;
            this.loadPage();
        },
        /**
         * 搜索音乐
         * */
        search: function () {
            var this_vue = this;
            $.ajax({
                url: '/get_search_result',
                data: {search_msgs: this_vue.search_msg},
                type: 'GET',
                dataType: 'JSON',
                beforeSend: function () {
                    layer.load();
                },
                success: function (data) {
                    layer.closeAll();
                    if (data.code == '000') {
                        layer.msg(data.msg, {icon: 0});
                        return false;
                    } else {
                        //添加搜索历史
                        if (!this_vue.search_history.includes(this_vue.search_msg)) {
                            this_vue.search_history.splice(0, 0, this_vue.search_msg);
                        } else {
                            this_vue.search_history.splice(this_vue.search_history.indexOf(this_vue.search_msg), 1);
                            this_vue.search_history.splice(0, 0, this_vue.search_msg);
                        }
                        var result = data.data.result;
                        this_vue.music_list = result.response.docs;
                        this_vue.is_searched = true;
                    }
                },
                error: function (xhr, type) {
                    layer.closeAll();
                    layer.msg('搜索貌似出错了...');
                }
            });
        },

        /**
         * 点击搜索历史
         * */
        click_history: function (msg) {
            this.search_msg = msg;
            this.search();
        },
        /**
         * 搜索框内容改变事件
         * */
        search_msg_change: function () {
            if (this.search_msg == '') {
                this.is_searched = false;
            }
        },
        /**
         * 播放音乐
         *
         * info：音乐信息
         * */
        paly_music: function (info) {
            var ap = new APlayer({
                container: document.getElementById('aplayer'),
                // lrcType: 3,//url形式
                lrcType: 1,
                audio: {
                    name: info.title || '',
                    artist: info.nickname || '',
                    url: info.play_path_aacv224 || info.play_path_aacv164 || info.play_path_64 || info.play_path_32,
                    cover: info.cover_path || '/static/images/music.png',
                    lrc: '[00:00.00]APlayer\n[00:04.01]is\n[00:08.02]amazing'
                }
            });
            ap.play();
        },
        paly_music_new: function (name, artist, url, cover, lrc) {
            console.log(name);
            console.log(artist);
            console.log(url);
            console.log(cover);
            var ap = new APlayer({
                container: document.getElementById('aplayer'),
                // lrcType: 3,//url形式
                lrcType: 1,
                audio: {
                    name: name,
                    artist: artist,
                    url: url,
                    cover: cover,
                    lrc: lrc
                }
            });
            ap.play();
        },
    },
    computed: {},
    mounted: function () {
        this.loadPage();
        this.loadData();
    }
});