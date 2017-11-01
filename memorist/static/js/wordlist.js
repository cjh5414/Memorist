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
    $.ajax({
        type: "POST",
        // url: "{% url 'wordlist:word_translate' %}",
        url: "/translate/",
        data: {'question': $("#id_question").val() },
        dataType: "json",
        success: function (response) {
            $("#id_answer").val(response.result);
        },
        error: function (request, status, error) {
            alert("API 요청 실패");
        }
    });
    $("#id_translate_result").text('번역 후');
});
