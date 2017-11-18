$("#id_study_confirm_btn").click(function () {
    $("#id_study_answer_block").show();
});

$("#id_study_next_btn").click(function () {
    $.ajax({
        type: "POST",
        url: "/study/next/",
        success: function (response) {
            $("#id_study_question_block").text(response.question);
            $("#id_study_answer_block").text(response.answer);
            $("#id_study_answer_block").hide();
        },
        error: function (request, status, error) {
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
                parent_tag.remove();
            }
        },
        error: function (request, status, error) {
            alert("API 요청 실패");
        }
    });
    location.reload();
});
