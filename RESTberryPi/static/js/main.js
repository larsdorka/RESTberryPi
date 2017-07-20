$(function () {
    $('#myTabs a[href="#static"]').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});

$(function () {
    $('#myTabs a[href="#apidoc"]').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $.ajax({
            url: "api",
            dataType: 'text',
            async: true,
            statusCode: {
                200: function (response) {
                    $("#apidoctextarea").val(response);
                }
            },
            error: function () {
                $("#apidoctextarea").val('error');
            }
        });
    });
});

$(function () {
    $.ajaxSetup({"contentType": "text/json"});
});

$(function () {
    $("[name=btn_chan]").click(gpioWrite_query);
});

function gpioWrite_query() {
    console.log($(this).attr('class'));
    const state = $(this).hasClass('btn-danger');
    if (!state) {
        $(this).removeClass('btn-success');
        $(this).addClass('btn-danger');
    } else {
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-success');
    }
    var params = "?channel=" + $(this).text().trim() + "&state=" + state.toString();
    $.get("api/gpioWrite" + params, function () {
    });
};
