/**
 * Created by Administrator on 2019-01-02.
 */
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#home",
    data: {
        msg: 'hello'
    },
    methods: {
        getmsg: function () {
            palyer_music('http://fdfs.xmcdn.com/group53/M02/B3/42/wKgLcVwSbVCCRayMAAx30wsoD2U375.mp3');
        },
    },
    computed: {},
    mounted: function () {
        this.getmsg();
    }
});