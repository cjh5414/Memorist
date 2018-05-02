function onClickPronounce(event, source) {
    event.stopPropagation();

    if (source !== '' && source !== undefined) {
        $.ajax({
            type: "POST",
            url: "/pronounce/",
            data: {'question': source},
            success: function (response) {
                var audio = new Audio(MEDIA_URL + response.file_name);
                audio.load();
                audio.play();
            },
            error: function (request, status, error) {
                console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                alert("API 요청 실패");
            }
        });
    }
}
