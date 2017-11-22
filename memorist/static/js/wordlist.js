$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$("#id_translate_button").click(function () {
    var question = $("#id_question").val();
    if(question.length!==0) {
        $.ajax({
            type: "POST",
            // url: "{% url 'wordlist:word_translate' %}",
            url: "/translate/",
            data: {'question': question},
            dataType: "json",
            success: function (response) {
                $("#id_answer").val(response.result);
            },
            error: function (request, status, error) {
                alert("API 요청 실패");
            }
        });
    }
});


$("#id_naver_dic_button").click(function () {
    var question = $("#id_question").val();
    window.open('http://endic.naver.com/search.nhn?sLn=kr&isOnlyViewEE=N&query=' + question, '_self');
});


$("#id_clear_button").click(function (){
    $("#id_question").val("");
    $("#id_answer").val("");
});


$(".delete_word_btn").click(function() {
    parent_tag = $(this).parent();

    $.ajax({
        type: "POST",
        url: "/words/" + $(this).data("id") + "/delete/",
        success: function (response) {
            if(response.result === "True") {
                parent_tag.remove();
            }
        },
        error: function (request, status, error) {
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            alert("API 요청 실패");
        }
    });
});


$(".restore_word_btn").click(function() {
    parent_tag = $(this).parent();

    $.ajax({
        type: "POST",
        url: "/words/" + $(this).data("id") + "/restore/",
        success: function (response) {
            if(response.result === "True") {
                parent_tag.remove();
            }
        },
        error: function (request, status, error) {
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            alert("API 요청 실패");
        }
    });
});
