var lastClickedWordTbody;

$(document).ready(function() {
    $("#id_question").focus();
});

$(".word_list_question, .word_list_answer").click(function() {
    tr = $(this).parent();
    tbody = tr.parent();

    tr.hide();
    tbody.find(".word_list_input_row").show();

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
