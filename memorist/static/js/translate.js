$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

$(document).ready(function() {
    $("#id_question").focus();
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


function onClickTranslatedResultList(word) {
    $("#id_answer").val($("#id_answer").val() + ", " + word);
}

$("#id_translate_button").click(function () {
    $("#id_glosbe_result_group").empty();
    $("#id_oxford_result_group").empty();

    var question = $("#id_question").val();
    if(question.length!==0) {
        $.ajax({
            type: "POST",
            // url: "{% url 'wordlist:word_translate' %}",
            url: "/translate/",
            data: {'question': question},
            dataType: "json",
            success: function (response) {
                $("#id_answer").val(response.papago_translation_result);
                if (response.glosbe_translation_result!==undefined) {
                    for (i=0; i<response.glosbe_translation_result.length; i++) {
                        $("#id_glosbe_result_group").append(
                            '<a href="#" class="list-group-item" onClick="onClickTranslatedResultList(\'' + response.glosbe_translation_result[i] + '\')">' +
                            response.glosbe_translation_result[i] + '</a>');
                    }
                }
                if (response.oxford_dictionary_result!==undefined) {
                    for (i=0; i<response.oxford_dictionary_result.length; i++) {
                        var entry = response.oxford_dictionary_result[i];

                        $("#id_oxford_result_group").append(
                            '<div>'
                        );

                        $("#id_oxford_result_group").append(
                            '<h3>' + (i+1) + '. ' + entry['definitions'][0] + '</h3>'
                        );

                        for (j=0; j<entry['examples'].length; j++) {
                            $("#id_oxford_result_group").append(
                                'ex) ' + entry['examples'][j] + '</br>'
                            );
                        }

                        $("#id_oxford_result_group").append(
                            '</div>'
                        );
                    }
                }
                $("#id_question").focus();
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
    $("#id_question").focus();
});


$("#id_exchange_button").click(function (){
    var question = $("#id_question").val();
    var answer = $("#id_answer").val();
    $("#id_question").val(answer);
    $("#id_answer").val(question);
    $("#id_question").focus();
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
