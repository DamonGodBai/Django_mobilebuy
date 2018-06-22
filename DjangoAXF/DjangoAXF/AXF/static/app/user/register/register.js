
$(function () {

    flag1 = false;  //检测用户名是否合法，默认不合法
    flag2 = false;  //检测密码是否合法，默认不合法
    flag3 = false;  //检测确认密码是否合法，默认不合法
    flag4 = false;  //检测邮箱是否合法，默认不合法

    // 用户名检测
    $('#username').change(function () {
        var uname = $(this).val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(uname)){
                flag1 = true;
        }
        else {
            flag1 = false;

            alert('用户名不合法');
        };
    });


    $('#password').change(function () {
        var psword = $(this).val();
        if (/^\w{8,}$/.test(psword)){
                flag2 = true;
        }
        else {
            flag2 = false;
            alert('请输入8位以上密码');
        };
    });


    $('#repassword').change(function () {
        var repasswd = $('#password').val()
        var psword = $(this).val();
        if (repasswd==psword){
                flag3 = true;
        }
        else {
            flag3 = false;
            alert('两次输入不一致');
        };
    });


    $('#email').change(function () {
        var email = $(this).val();
        if (/^\w+@\w+\.\w+$/.test(email)){
                flag4 = true;
        }
        else {
            flag4 = false;
            alert('邮箱不合法，请重新输入');
        };
    });


$('form').submit(function () {
    if (flag1 && flag2 && flag3 && flag4){
        $('#password').val(md5($('#password').val()));
        console.log($('#password').val())
        return true
    }
    else {
        alert('输入内容不合法')
        return false
    }
});

$('#username').change(function () {
    if(flag1) {
       $.get('/app/checkusername/', {'username': $(this).val()}, function (data) {
            // console.log(data);
            // 可以使用
            if (data.status == 1) {
                $('#username_errmsg').html(data.msg).css('color', 'green')
            }
            //    不可以使用
            else if (data.status == 0) {
                $('#username_errmsg').html(data.msg).css('color', 'red')
            }
        })
    }

    else {
        $('#username_errmsg').html("")
    }
})


});