$(function () {
    $('#myTabs a[href="#gpio"]').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        startIntervalRead();
    });
});

$(function () {
    $('#myTabs a[href="#apidoc"]').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        stopIntervalRead();
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
    const state = $(this).hasClass('btn-danger');
    if (!state) {
        $(this).removeClass('btn-success');
        $(this).addClass('btn-warning');
    } else {
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-warning');
    }
    var params = "?channel=" + $(this).text().trim() + "&state=" + state.toString();
    $.get("api/gpioWrite" + params, function () {
    });
};

var intervalReadFunction;

function startIntervalRead() {
    intervalReadFunction = setInterval(gpioRead_query, 1000)
}

function stopIntervalRead() {
    clearInterval(intervalReadFunction);
}

$(function () {
    startIntervalRead();
});

function gpioRead_query() {
    $.get("api/gpioReadAll", function (response) {
        const responseObj = JSON.parse(response);
        if (responseObj !== null && responseObj.length > 0) {
            const myButtons = $("[name=btn_chan]");
            for (var index = 0; index < myButtons.length; index++) {
                if (index < responseObj.length) {
                    if (responseObj[index] === true) {
                        $(myButtons[index]).removeClass('btn-warning');
                        $(myButtons[index]).addClass('btn-success');
                    } else {
                        $(myButtons[index]).removeClass('btn-warning');
                        $(myButtons[index]).addClass('btn-danger')
                    }
                }
            }
        }
    });
}
