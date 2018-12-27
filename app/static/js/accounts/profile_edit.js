$(document).on('ready', function() {
    $('#login').prop('disabled', true);

    setRoleDescription($('#role'));
    $('#role').on('change', function() { setRoleDescription($(this)); });
    $('#saveuser').on('click', function() { $('.form').submit(); });

    $('#deleteuser').on('click', function() {
        if (confirm('are you sure to delete?')) $('#form_deleteuser').submit();
    });

    $('#resetpassword').on('click', function() {
        if (confirm('are you sure to reset pass?')) $('#form_resetpassword').submit();
    });

    function setRoleDescription(roleitem) {
        var roles = {
            "3": "edit allow",
            "2": "editing not allowed ",
            "1": "only user info",
        };
        $('#role-description').html(roles[roleitem.val()]);
    }
});
