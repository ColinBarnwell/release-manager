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
                document.open('text/html', 'replace');
                document.write(response);
                document.close();
            } else {
                $(target_id).html(response);
            }

        }
    });
}

$(function() {

    var current_location = document.location.pathname + document.location.search;

    if (request_location !== undefined && request_location != current_location) {
        window.history.replaceState('', '', request_location);
    }

    $('body').on('click', '[data-ajax-url]', function() {
        ajax_load($(this).attr('data-ajax-url'), $(this).attr('data-ajax-target'));
        if ($(this).attr('data-ajax-param')) {
            window.history.replaceState('', '', document.location.pathname + '?' + $(this).attr('data-ajax-param'));
        }
        $(this).parents('table').find('tr').removeClass('warning');
        $(this).addClass('warning');
        return false;
    });

    $('body').on('click', '[data-modal-url]', function() {
        ajax_load($(this).attr('data-modal-url'), '#form-modal-content', function() {$('#form-modal').modal();});
        return false;
    });

    $('body').on('click', '[data-ajax-submit]', function() {
        ajax_submit($('#modal-form'), '#form-modal-content');
        return false;
    });
});
