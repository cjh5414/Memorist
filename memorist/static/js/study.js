$("#id_study_confirm_btn").click(function () {
    $("#id_study_answer_block").show();
});

$("#id_study_next_btn").click(function () {
    location.reload();
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
