$("#password").on("focusout", function (e) {
    if ($(this).val() != $("#passwordConfirm").val()) {
        $("#passwordConfirm").removeClass("valid").addClass("invalid");
        $('.submit-button').prop('disabled', true);
    } else {
        $("#passwordConfirm").removeClass("invalid").addClass("valid");
        $('.submit-button').prop('disabled', false);
    }
});

$("#passwordConfirm").on("keyup", function (e) {
    if ($("#password").val() != $(this).val()) {
        $(this).removeClass("valid").addClass("invalid");
        $('.submit-button').prop('disabled', true);
    } else {
        $(this).removeClass("invalid").addClass("valid");
        $('.submit-button').prop('disabled', false);
    }
});