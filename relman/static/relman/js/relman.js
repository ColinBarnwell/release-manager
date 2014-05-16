function ajax_load(url, target_id) {
    $.ajax({
        type: 'GET',
        url: url,
        cache: false,
        success: function(response) {
            $(target_id).html(response);
        }
    });
}


$(function() {
    $('body').on('click', '[data-ajax-url]', function() {
        ajax_load($(this).attr('data-ajax-url'), $(this).attr('data-ajax-target'));
    });
});