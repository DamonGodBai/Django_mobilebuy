$(function () {

    // 点击全部类型
    $('#all_type').click(function () {
        $("#all_type_container").toggle();  // 切换显示和隐藏
        $('#all_type_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        // $('#sort_rule_container').hide();
        // $('#sort_rule_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        // 主动触发$('#sort_rule_container')的click事件
        $('#sort_rule_container').triggerHandler('click')

    });

    $("#all_type_container").click(function () {
        $(this).hide();  // 隐藏
        $('#all_type_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    });

    // 点击综合排序
    $('#sort_rule').click(function () {
        $('#sort_rule_container').toggle();
        $('#sort_rule_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        // 主动触发$('#all_type_container')的click事件
        $('#all_type_container').triggerHandler('click')
    });

    $('#sort_rule_container').click(function () {
        $(this).hide();
        $('#sort_rule_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    });


    // 商品数量的增加
    $('.addnum').click(function () {
        numNode = $(this).parent().find('.num');
        num = parseInt(numNode.html()) + 1;
        numNode.html(num)
    });

    // 商品数量的减少
    $('.subnum').click(function () {
        numNode = $(this).parent().find('.num');
        num = parseInt(numNode.html()) - 1;
        if (num < 1) {
            num = 1
        }
        numNode.html(num)
    })

    $('.addtocart').click(function () {

        //获取当前点击的商品id
        goodsid = $(this).attr('goodsid');
        //获取当前商品的数量
        /*
        index = $(this).index('.addtocart');
        //console.log(index)
        numNode = $('.num').eq(index);
        */
        numNode = $(this).prev().find('.num');
        num = parseInt(numNode.html());

        $.get('/app/add_to_cart', {'goodsid': goodsid, 'num': num}, function (data) {
            //添加成功
            console.log(data)
            if (data.status == 1) {
                alert(data.msg);
            }
            //用户未登录
            else if (data.status == -1) {
                res = confirm('请先登录');
                if (res) {
                    //    跳转到登录
                    location.href = '/app/login'
                }
            }
            else {
                alert('加入购物车失败')
            }
        })

    })

});
