/**
 * Created by chucho on 14/09/19.
 */
//dropdown obj
var dropdown = $(document.currentScript.dataset.dropdown);
var dropdown_table = $(document.currentScript.dataset.table);

$(document).ready(function () {

    dropdown = dropdown.length > 0 ? dropdown : $('#actions_dropdown');
    dropdown_table = dropdown_table.length > 0 ? dropdown_table : $('.table');

    if (dropdown.length > 1) {
        // console.error("Multiple dropdown objects found. Please provide an identifier to match a single dropdown");
    }

    if (dropdown_table.length > 1) {
        // console.error("Multiple dropdown table objects found. Please provide an identifier to match a single dropdown table");
    }

    function toggleActionDropdown() {

        if ($('.table tbody input:checked').length > 0) {
            dropdown.removeClass('disabled');

        } else {
            dropdown.addClass('disabled');
        }
    }

    function clearHiddenInputs(form) {
        form.find("input.extra").remove();
    }

    function createHiddenInput(form, val) {
        var input = $('<input>')
            .attr('class', 'extra')
            .attr('type', 'hidden')
            .attr('name', 'selection[]').val(val);
        form.append(input);
    }

    function toggleHeaderCheckbox() {
        //prop header checkbox if all are check else uncheck
        var checked = $('td input:checkbox:checked');
        var total = $('td input:checkbox');
        if (checked.length === total.length) {
            dropdown_table.find("th input:checkbox").prop('checked', true);
        } else {
            dropdown_table.find("th input:checkbox").prop('checked', false);

        }
    }

    // initialize dropdown on page ready
    toggleActionDropdown();

    // table header checkbox
    // disables/enables all checkbox selections
    dropdown_table.find("th input:checkbox").change(function () {
        dropdown_table.find("input[name=selection]").prop('checked', $(this).prop("checked"));
        dropdown_table.find("input[name=selection]").trigger('change');
        toggleActionDropdown();
    });

    // table body checkboxes
    dropdown_table.find("td input:checkbox").change(function () {
        toggleActionDropdown();
        toggleHeaderCheckbox()
    });


    function set_form_action(form, button) {
        var url = button.attr('href');

        form.attr('action', url);
        // uses method defined in dropdown link action for the form submit
        if ($button.data('method'))
            form.attr('method', $(this).data('method'));
        return form;
    }

    function add_hidden_inputs(form) {
        // clears any pre added inputs
        clearHiddenInputs(form);

        $('.table input:checked').each(function (_, el) {
            var val = $(el).val();
            if (val != 'on') {
                createHiddenInput(form, val);
            }
        });
    }

    function form_submit(form, button) {
        add_hidden_inputs(form);
        set_form_action(form, button);
        // submits the form to the url provided in the dropdown action link
        form.submit();
    }

    function init_swal(title, content, confirm_text, confirm_button_color) {
        var options = {
            customClass: {
                confirmButton: confirm_button_color ? "btn btn-sm btn-" + confirm_button_color : "btn btn-sm btn-danger",
                cancelButton: 'btn btn-sm btn-light-primary'
            },
            buttonsStyling: false,
            title: title ? title : gettext("Are you sure?"),
            text: content || content==="" ? content : gettext("You won't be able to revert this!"),
            icon: "question",
            showCancelButton: true,
            confirmButtonText: confirm_text ? confirm_text : gettext("Yes, delete it!"),
            backdrop: true,

        };

        return Swal.mixin(options);

    }

    // dropdown action click
    $(document).on('click', 'a.apply-bulk-action', function (e) {
        e.preventDefault();
        e.stopPropagation();

        $button = $(this);

        var title = $button.data('title');
        var content = $button.data('content');
        var confirm_text = $button.data('confirm_text');
        var skip_confirm = $button.data('skip_confirm');
        var confirm_button_color = $button.data('confirm_button_color');
        var form = dropdown.closest('.dropdown').find('form.actions-form');
        console.log(form);

        // skip confirmation and submit form immediately
        if (typeof (skip_confirm) != 'undefined') {
            form_submit(form, $button);
            return;
        }

        const swalWithBootstrapButtons = init_swal(title, content, confirm_text, confirm_button_color);

        swalWithBootstrapButtons.fire().then((result) => {
            if (result.value) {
                form_submit(form, $button);
            }
        })
    });

})