/**
 * Created by Administrator on 2019-01-02.
 */
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#search",
    data: {
        msg: 'hello',
        search_msg: ''
    },
    methods: {
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
                    var result=data.data.result;
                    console.log(result.track.docs);
                },
                error: function (xhr, type) {
                    layer.closeAll();
                    layer.msg('搜索貌似出错了...');
                }
            });
        },
        getmsg: function () {
            palyer_music('http://fdfs.xmcdn.com/group53/M02/B3/42/wKgLcVwSbVCCRayMAAx30wsoD2U375.mp3');
        },
    },
    computed: {},
    mounted: function () {
        this.getmsg();
    }
});