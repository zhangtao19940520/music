/**
 * Created by Administrator on 2019-01-02.
 */
$(function () {
    var urlpath = window.location.pathname;
    var navs = $('.navs a');
    navs.each(function () {
        var data_url = $(this).attr('href');
        if (urlpath == data_url) {
            $('.navs a .active').removeClass('active');
            $(this).addClass('active');
        }
    });
});

function palyer_music(url) {
    layer.alert(url);
    var ap3 = new APlayer({
        element: document.getElementById('player'),//样式1
        narrow: false,
        autoplay: false,
        showlrc: true,
        music: {
            title: 'Jar Of Love',
            author: '_Re-梦_',
            // url: '/static/aa.mp3',
            // url: 'http://fdfs.xmcdn.com/group53/M02/B3/42/wKgLcVwSbVCCRayMAAx30wsoD2U375.mp3',
            url: url,
            pic: '/static/zz.jpg'
        }
    });
    ap3.init();
}
