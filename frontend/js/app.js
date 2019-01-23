$(document).ready(() => {
    $('#order-form').submit(function(event) {
       $(this).addClass('loading');
       $('#submit-button').addClass('loading');
    });
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
});
