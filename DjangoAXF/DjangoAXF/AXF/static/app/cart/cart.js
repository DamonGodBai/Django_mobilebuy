$(function () {
    // 增加
    $('.add_num').click(function () {

        var that = this;
        //获取当前点击商品的购物车id
        cartid = $(this).parents('li').attr('cartid');

        // 让后台将当前的数量num+1
        $.getJSON('/app/addnum/', {'cartid': cartid}, function (data) {
            if (data.status == 1) {
                // 成功
                $(that).parent().find('.num').html(data.num)

                if (parseInt(data.num) > 1) {
                    $(that).parent().find('.sub_num').prop('disabled', false);
                    $(that).parent().find('.sub_num').css('background', 'white');

                }
            }

            // 重新计算总价
            calculateTotalPrice();
        });
    });


//减少
    $('.sub_num').click(function () {

        var that = this;
        //判断数量是否为1
        //1、如果为1.则禁止'减少'的按钮
        //2、如果大于1，则应该解除
        var num = $(this).parent().find('.num').html();
        if (parseInt(num) > 1) {

            //获取当前点击商品的购物车id
            cartid = $(this).parents('li').attr('cartid');

            // 让后台将当前的数量num+1
            $.getJSON('/app/subnum/', {'cartid': cartid}, function (data) {
                if (data.status == 1) {
                    // 成功
                    $(that).parent().find('.num').html(data.num)
                    if (parseInt(data.num) <= 1) {
                        $(that).prop('disabled', true); //禁用
                        $(that).css('background', 'grey')
                    }
                }

                // 重新计算总价
                calculateTotalPrice();

            });
        }
    });


    // 勾选/取消勾选
    $('.is_choice').click(function () {
        var that = this
        cartid = $(this).parents('li').attr('cartid');

        //    请求服务器将勾选状态改变

        $.get('/app/changeselectstate/', {'cartid': cartid}, function (data) {
            // console.log(data)
            if (data.status == 1) {
                if (data.select == 1) {
                    $(that).find('span').html('√')
                }
                else {
                    $(that).find('span').html('')

                }
            }
            // 更新‘全选’按钮的选中状态
            isAllSelected();

        })
    })

//    删除
    $('.delbtn').click(function () {
        var that = this
        cartid = $(this).parents('li').attr('cartid');
        console.log(cartid)
        $.get('/app/cartdelgoods/', {'cartid': cartid}, function (data) {

            if (data.status == 1) {
                $(that).parents('li').remove()
            }
            // 更新全选按钮
            isAllSelected();
        })
    })

//    全选、全不选
    $('#all_select').click(function () {
        // 1.如果全部勾选，则执行‘全不选’操作
        //    2.如果有没有勾选的，则执行‘全选操作’
        selects = [];
        unselects = [];

        $('.menuList').each(function () {
            var gou = $(this).find('.is_choice').find('span').html();

            if (gou) {
                selects.push($(this).attr('cartid'))
            }
            else {
                unselects.push($(this).attr('cartid'))
            }
        });
        // console.log(selects)
        //  console.log(unselects)
        //  全不选
        if (unselects.length == 0) {
            //    请求服务器，将selects中所有cartid上传给服务器
            $.get('/app/cartchangeselect/', {'selects': selects.join('#'), 'action': "unselect"}, function (data) {
                // console.log(data)
                if (data.status == 1) {
                    $('.is_choice').find('span').html('')
                }
                // 更新‘全选’按钮的选中状态
                isAllSelected();
            })
        }
        // 全选
        else {
            $.get('/app/cartchangeselect/', {'selects': unselects.join('#'), 'action': 'select'}, function (data) {
                if (data.status == 1) {
                    $('.is_choice').find('span').html('√')
                }
                // 更新‘全选’按钮的选中状态
                isAllSelected();
            })
        }

    })


    isAllSelected();

//    检测是否全选
    function isAllSelected() {

        count = 0;
        $('.is_choice').each(function () {
            if ($(this).find('span').html()) {
                count++;
            }
        });

        if (count == $('.is_choice').length) {
            $('#all_select_icon').html('√')
        }
        else {
            $('#all_select_icon').html('')

        }
        // 总价
        calculateTotalPrice();
    }

    // 计算总价
    function calculateTotalPrice() {
        totalprice = 0;
        // 遍历每个购物车商品
        $('.menuList').each(function () {
            if ($(this).find('.is_choice span').html()) {
                price = $(this).find('.price').html();
                num = $(this).find('.num').html();
                totalprice += parseFloat(price) * parseFloat(num)
            }
        })

        //显示总价
        $('#totalprice').html(totalprice.toFixed(2));
    }


    // 结算
    $('#calculate').click(function () {
        selects = [];
        // 遍历购物车中所有id,提取选中商品
        $('.menuList').each(function () {
            if ($(this).find('.is_choice span').html()) {
                selects.push($(this).attr('cartid'))
            }
        });
        console.log(selects)
        if (selects.length == 0) {
            alert('请先选择商品');
            return
        }

        //请求服务器，将选中商品cartid提交，并让服务器生成订单
        $.get('/app/generateorder/', {selects: selects.join('#')}, function (data) {
            console.log(data)
            if (data.status == 1) {
                location.href = '/app/orderinfo/' + data.orderid + '/'
            }
            // 没有登录
            else if (data.status == -1) {
                alert(data.msg)
            }


        })

    })
    // 生成订单成功

});