$(function () {

    $('#pay').click(function () {

        // 去支付宝，微信支付 （一般以企业作为商家跟支付宝或微信合作）
        // 以支付宝为例：
        //      1, 点击支付
        //      2, 调用支付宝提供的接口并提交参数(订单标题，订单号，订单总金额，
        //          收款的支付宝ID, 商户ID, 回调url:用来接收支付结果) 给支付宝,
        //          支付宝会让用户支付，并在支付完成后将money转到你的收款支付宝账号上，
        //          并通过商户提供的回调url来通知商户是否支付成功. 然后在商户将该订单号
        //          对应的订单状态更改.

        // 伪支付
        orderid = $(this).attr('orderid');

        $.get('/app/changeorderstatus/', {orderid:orderid, status:'1'}, function (data) {
            // 改变订单状态成功，则进入'我的'页面
            if (data.status == 1){
                location.href = '/app/mine/'
            }

        })



    })

});