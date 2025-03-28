function addLike(pk) {
    console.log($("#csrf").serializeArray()[0]["value"]);
    console.log(pk);
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': $("#csrf").serializeArray()[0]["value"]
        }
    });
    $.ajax({
        url: "/dorm_guide/add-like/",
        type: "POST",
        data: {"pk": pk}
    }).done(function (response) {
        console.log(response);
    });

    $("#like-count-" + pk.toString()).text(parseInt($("#like-count-" + pk.toString()).text()) + 1);
}
