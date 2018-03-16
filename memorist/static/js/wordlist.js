var lastClickedWordTbody;

$(document).ready(function() {
    $("#id_question").focus();
});

$(".word_list_question, .word_list_answer").click(function() {
    tr = $(this).parent();
    tbody = tr.parent();

    question = tr.find(".word_list_question").text();
    answer = tr.find(".word_list_answer").text();

    tr.hide();

    input_tr = tbody.find(".word_list_input_row");

    input_tr.show();
    input_tr.find(".word_list_input_question").val(question);
    input_tr.find(".word_list_input_answer").val(answer);

    if(this.className==="word_list_question")
        input_tr.find(".word_list_input_question").focus();
    else
        input_tr.find(".word_list_input_answer").focus();

    lastClickedWordTbody = tbody;
});

$(document).mouseup(function (e){
    if(lastClickedWordTbody !== undefined) {
        var container = lastClickedWordTbody;
        if (container.has(e.target).length === 0) {
            container.find(".word_list_row").show();
            container.find(".word_list_input_row").hide();
        }
    }
});

$(".edit_word_btn").click(function() {
    original_question = lastClickedWordTbody.find(".word_list_question").text();
    original_answer = lastClickedWordTbody.find(".word_list_answer").text();
    edited_question = lastClickedWordTbody.find(".word_list_input_question").val();
    edited_answer = lastClickedWordTbody.find(".word_list_input_answer").val();

    if(original_question!==edited_question || original_answer!==edited_answer) {
        $.ajax({
            type: "POST",
            url: "/words/" + $(this).data("id") + "/edit/",
            data: {
                'question': edited_question,
                'answer': edited_answer
            },
            dataType: "json",
            success: function (response) {
                if(response.result === "True") {
                    lastClickedWordTbody.find(".word_list_question").text(edited_question);
                    lastClickedWordTbody.find(".word_list_answer").text(edited_answer);
                    lastClickedWordTbody.find(".word_list_row").show();
                    lastClickedWordTbody.find(".word_list_input_row").hide();
                }
            },
            error: function (request, status, error) {
                console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                alert("API 요청 실패");
            }
        });
    }
});
