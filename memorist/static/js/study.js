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
