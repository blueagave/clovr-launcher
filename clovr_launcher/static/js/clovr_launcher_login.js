$(document).ready( function() {
    $('#toggle_help').on('click', function(e) {
        e.preventDefault();
        $('body').chardinJs('toggle');
    });
});
