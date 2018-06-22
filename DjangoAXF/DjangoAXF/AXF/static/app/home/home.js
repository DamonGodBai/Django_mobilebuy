$(document).ready(function () {
        setTimeout( function () {
            swiper1()
        }, 100)
})

function swiper1() {
    var mySwiper1 = new Swiper('#topSwiper',{
        direction : 'horizontal',
        speed:2000,
        loop: true,
        autoplay:true,
        pagination:'.swiper-pagination',
        control:true,
    })

    var mySwiper1 = new Swiper('#swiperMenu',{
        slidesPerView: 3
    })
}