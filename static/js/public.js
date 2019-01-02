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

/**
 * 播放音乐的公用方法
 * */
function palyer_music(url) {
    var ap3 = new APlayer({
        element: document.getElementById('player'),//样式1
        narrow: false,
        autoplay: false,
        showlrc: true,
        music: {
            title: 'Jar Of Love',
            author: '_Re-梦_',
            url: url,
            pic: '/static/zz.jpg'
        }
    });
    ap3.init();
}
