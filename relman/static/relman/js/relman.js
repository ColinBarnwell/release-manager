function ajax_load(url, target_id, callback) {
    $.ajax({
        type: 'GET',
        url: url,
        cache: false,
        success: function(response) {
            $(target_id).html(response);
            if (callback !== undefined) {
                callback();
            }
        }
    });
}

function ajax_submit(form, target_id) {
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function(response) {
            if (response.indexOf('<!DOCTYPE html>') > 0) {
                // Quick and dirty replace of the body element if the response
                // contains a complete document (assumes same <head> content)
                $('body').html($(response, 'body'));
                $('body').removeClass();
            } else {
                $(target_id).html(response);
            }

        }
    });
}

$(function() {
    $('body').on('click', '[data-ajax-url]', function() {
        ajax_load($(this).attr('data-ajax-url'), $(this).attr('data-ajax-target'));
        $(this).parents('table').find('tr').removeClass('warning');
        $(this).addClass('warning');
    });
    $('body').on('click', '[data-modal-url]', function() {
        ajax_load($(this).attr('data-modal-url'), '#form-modal-content', function() {$('#form-modal').modal();});
    });
    $('body').on('click', '[data-ajax-submit]', function() {
        ajax_submit($('#modal-form'), '#form-modal-content');
        return false;
    });
});