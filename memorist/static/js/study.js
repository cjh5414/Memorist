$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/accounts/studystatus/",
        async: false,
        success: function (response) {
            $("#id_study_question_types input[value=" + response.question_type + "]").prop("checked", true);
            $("#id_study_filtered_by_days option[value=" + response.chosen_days + "]").prop("selected", true);
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });

    updateStudyProgressBar();

    setNumberOftestWordSelect();
});

$("#id_study_confirm_btn").click(function () {
    $("#id_study_answer_block").show();
});

function getNextWord() {
    $.ajax({
        type: "GET",
        url: "/study/next/",
        success: function (response) {
            if (response.errorType && response.errorType === "NotExist") {
                alert("해당 되는 단어가 없습니다.");
            }
            else {
                $("#id_study_remove_btn").data("id", response.id);
                $("#id_study_question_block").text(response.question);
                $("#id_study_answer_box").text(response.answer);
                $("#id_study_answer_block").hide();
            }
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
}

$("#id_study_next_btn").click(getNextWord);

$("#id_study_remove_btn").click(function () {
    $.ajax({
        type: "POST",
        url: "/words/" + $(this).data("id") + "/delete/",
        async: false,
        success: function (response) {
            if (response.result === "True") {
                getNextWord();
            }
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });

    updateStudyProgressBar();
});

$("#id_make_test_btn").click(function () {
    var question_number = $("#id_test_words_number_select option:selected").text();
    test_table = $("#id_test_table");

    $("#id_check_test_answer_btn").prop("disabled", false);
    $("#id_test_table .test_answer").hide();
    $("#id_check_test_answer_btn").text("답 확인");
    $("#id_check_test_answer_btn").val("off");
    $("#id_test_table tr").slice(1).remove();

    $.ajax({
        type: "GET",
        url: "/study/test/",
        data: {
            num: question_number
        },
        success: function (response) {
            test_word_list = response.testWordList;
            for (i = 0; i < test_word_list.length; i++) {
                test_table.append(
                    '<tr onClick="onClickTestCol(\'' + i + '\')">' +
                    '<td></td>' +
                    '<td>' + test_word_list[i].question + ' ' +
                    '<a href="#" onClick="onClickPronounce(event, \'' + test_word_list[i].question + '\')"><span class="glyphicon glyphicon-volume-up pronounce" style=""></span></a>' +
                    '</td>' +
                    '<td><span class="test_answer" hidden>' + test_word_list[i].answer + ' ' +
                    '<a href="#" onClick="onClickPronounce(event, \'' + test_word_list[i].answer + '\')"><span class="glyphicon glyphicon-volume-up pronounce" style=""></span></a>' +
                    '</span></td>' +
                    '</tr>')
            }
            test_table.show();
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
});

function onClickTestCol(index) {
    trs = $("#id_test_table, tr");
    test_answer = trs.eq(parseInt(index) + 2).find(".test_answer");
    test_answer.toggle();
}

$("#id_check_test_answer_btn").click(function () {
    var answer_status = $(this).val();
    if (answer_status === "on") {
        $("#id_test_table .test_answer").hide();
        $(this).text("답 확인");
        $(this).val("off");
    }
    else {
        $("#id_test_table .test_answer").show();
        $(this).text("답 제거");
        $(this).val("on");
    }
});

$("#id_test_words_number_select").change(function () {
    $("#id_make_test_btn").prop("disabled", false);
});

$("#id_study_question_types").change(function () {
    var question_type = $("#id_study_question_types input[name='question_type']:checked").val();

    $.ajax({
        type: "POST",
        url: "/accounts/studystatus/update-question-type/",
        data: {
            'question_type': question_type
        },
        async: false,
        success: function (response) {

        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });

    setNumberOftestWordSelect();
});

$("#id_study_filtered_by_days").change(function () {
    var chosen_days = $("#id_study_filtered_by_days option:selected").val();

    $.ajax({
        type: "POST",
        url: "/accounts/studystatus/update-chosen-days/",
        data: {
            'chosen_days': chosen_days
        },
        success: function (response) {

        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });

    setNumberOftestWordSelect();
});

function setNumberOftestWordSelect() {
    words_number_select = $("#id_test_words_number_select");
    $("#id_make_test_btn").prop("disabled", true);
    $("#id_check_test_answer_btn").prop("disabled", true);

    $.ajax({
        type: "GET",
        url: "/study/numberofwords/",
        success: function (response) {
            words_number_select.find('option').remove().end().append(
                '<option disabled selected>Num</option>' +
                '<option>All</option>');
            for (var i = 0; i < response.numberOfWords; i++) {
                words_number_select.append(
                    '<option>' + (i + 1) + '</option>'
                )
            }
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
}

function updateStudyProgressBar() {
    $.ajax({
        type: "GET",
        url: "/study/progress/",
        async: false,
        success: function (response) {
            $("#id_study_progress_studied_num").text(response.studiedNumberOfWords);
            $("#id_study_progress_total_num").text(response.totalNumberOfWords);
            var percentage = response.studiedNumberOfWords/response.totalNumberOfWords*100;
            if(percentage > 49)
                $("#id_study_progress_text").removeClass("progress_text");
            else
                $("#id_study_progress_text").addClass("progress_text");

            $("#id_study_progress_percentage").text(percentage.toFixed(1));
            $("#id_study_progress_bar").css("width", percentage + "%");
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
}