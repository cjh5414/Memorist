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
