$(document).ready(function () {


    function fail_response(resp, error_text) {

        var msg = error_text ? error_text : gettext("Sorry, an Error has occurred during the operation. We are working on It.")

        if (resp.status === 403) {
            window.location.reload();
        } else if (resp.status === 404) {
            swal.fire({
                title: gettext('Error'),
                text: gettext("Not found"),
                icon: 'error',
            }).then(function () {
                window.location.reload();

            });
        } else {
            var resp_json = resp.responseJSON;
            if (resp_json) {
                if (resp_json.msg) {
                    msg = resp_json.msg;
                } else {
                    msg = resp_json;
                }
            }

            swal.fire({
                title: gettext('Error!'),
                text: msg,
                icon: 'error',
            });
        }
    }

    function ajax_call(url, method, success_text, error_text, btn, btn_process) {

        $.ajax({
            url: url,
            type: method ? method : 'POST',
        })
            .done(function (resp, status_msg, resp_obj) {
                const resp_json = resp_obj.responseJSON;
                let msg = success_text ? success_text : gettext('The operation completed successfully.');
                let redirect_to;
                if (resp_json) {
                    msg = resp_json.msg ? resp_json.msg : msg;
                    redirect_to = resp_json.redirect_to;
                }

                blockUI.release();

                swal.fire({
                    title: gettext('Success!'),
                    text: msg,
                    icon: 'success',
                }).then(function (resp) {

                    if (redirect_to !== undefined && redirect_to !== "") {
                        window.location = redirect_to;
                    } else {
                        window.location.reload();
                    }
                });

            })
            .fail(function (resp) {

                fail_response(resp, error_text);
                blockUI.release();
            });

    }

    function init_swal(title, content, confirm_text, confirm_button_color) {
        var options = {
            customClass: {
                confirmButton: confirm_button_color ? "btn btn-sm btn-" + confirm_button_color : "btn btn-sm btn-danger",
                cancelButton: 'btn btn-sm btn-light-primary'
            },
            buttonsStyling: false,
            title: title ? title : gettext("Are you sure?"),
            text: content || content === "" ? content : gettext("You won't be able to revert this!"),
            icon: "question",
            showCancelButton: true,
            confirmButtonText: confirm_text ? confirm_text : gettext("Yes, delete it!"),
            backdrop: true,
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,

        };

        return Swal.mixin(options);

    }

    // Generic action button
    $(document).on('click', 'a.delete-button', function (e) {
        e.preventDefault();
        $button = $(this);
        var url = $button.attr('href');
        var object_id = $button.data('id');
        var title = $button.data('title');
        var content = $button.data('content');
        var confirm_text = $button.data('confirm_text');
        var success_text = $button.data('success_text');
        var error_text = $button.data('error_text');
        var method = $button.data('method');
        var skip_confirm = $button.data('skip_confirm');
        var confirm_button_color = $button.data('confirm_button_color');
        var btn_process = $button.data('btn_process');

        // skip confirmation and make ajax_call immediately
        if (typeof (skip_confirm) != 'undefined') {
            ajax_call(url, method, success_text, error_text, $button, btn_process);
        }

        const swalWithBootstrapButtons = init_swal(title, content, confirm_text, confirm_button_color);
        swalWithBootstrapButtons.fire().then(
            function (e) {

                if (e.value) {
                    blockUI.block();
                    ajax_call(url, method, success_text, error_text, $button, btn_process);
                }
            });
    });
});
