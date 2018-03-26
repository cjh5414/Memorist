$("#id_study_confirm_btn").click(function () {
    $("#id_study_answer_block").show();
});

$("#id_study_next_btn").click(function () {
    var question_type = $("#id_study_question_types input[name='question_type']:checked").parent().text();

    $.ajax({
        type: "POST",
        url: "/study/next/",
        data: {'questionType': question_type},
        success: function (response) {
            $("#id_study_remove_btn").data("id", response.id);
            $("#id_study_question_block").text(response.question);
            $("#id_study_answer_block").text(response.answer);
            $("#id_study_answer_block").hide();
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
});

$("#id_study_remove_btn").click(function () {
    $.ajax({
        type: "POST",
        url: "/words/" + $(this).data("id") + "/delete/",
        success: function (response) {
            if (response.result === "True") {
                location.reload();
            }
        },
        error: function (request, status, error) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            alert("API 요청 실패");
        }
    });
});

$("#id_make_test_btn").click(function () {
    var number = 4;
    $("#id_test_table tr").remove();

     test_table= $("#id_test_table");
     test_table.append(
        '<tr>' +
            '<th>#</th>' +
            '<th>Question</th>' +
            '<th>Answer</th>' +
            '<th></th>' +
        '</tr>');

    $.ajax({
        type: "GET",
        url: "/study/test/",
        data: {
            num: number
        },
        success: function (response) {
            test_word_list = response.testWordList;
            for (i = 0; i < number; i++) {
                test_table.append(
                    '<tr>' +
                        '<td></td>' +
                        '<td>' + test_word_list[i].question + '</td>' +
                        '<td>' + test_word_list[i].answer + '</td>' +
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
