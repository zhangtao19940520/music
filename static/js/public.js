/**
 * Created by Administrator on 2019-01-02.
 */
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        search_msg: '',
        music_list: [],
        is_searched: false,//是否执行了搜索功能
        show_page: 'home',//默认显示首页
        search_history: [],//搜索历史
    },
    methods: {
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
                    //搜索历史
                    if (data.search_history.length > 0) {
                        this_vue.search_history = data.search_history.split(',').reverse();
                    }
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
                        layer.msg(data.msg);
                        return false;
                    }
                    else {
                        //添加搜索历史
                        if (!this_vue.search_history.includes(this_vue.search_msg)) {
                            this_vue.search_history.splice(0, 0, this_vue.search_msg);
                        }
                        else {
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
         * 点击搜素历史
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
            const ap = new APlayer({
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
    },
    computed: {},
    mounted: function () {
        this.loadPage();
        this.loadData();
    }
});