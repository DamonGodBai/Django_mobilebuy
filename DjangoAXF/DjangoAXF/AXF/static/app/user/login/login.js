
$(function () {
    $('form').submit(function () {
        $('#password').val(md5($('#password').val()))
    })
})