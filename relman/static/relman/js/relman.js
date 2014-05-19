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


$(function() {
    $('body').on('click', '[data-ajax-url]', function() {
        ajax_load($(this).attr('data-ajax-url'), $(this).attr('data-ajax-target'));
        $(this).parents('table').find('tr').removeClass('warning');
        $(this).addClass('warning');
    });
    $('body').on('click', '[data-modal-url]', function() {
        ajax_load($(this).attr('data-modal-url'), '#form-modal-content', function() {$('#form-modal').modal();});
    });
});