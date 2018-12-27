$(document).on('ready', function() {
    $('.edituser').on('click', function() {
        var id = $(this).attr('id');
        location.href = Flask.url_for('accounts.edituser', { "user_id": id });
    });
});
