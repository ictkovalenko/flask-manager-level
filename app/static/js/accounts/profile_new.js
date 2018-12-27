$(document).on('ready', function() {
    setRoleDescription($('#role'));
    $('#role').on('change', function() { setRoleDescription($(this)); });
    $('#newuser').on('click', function() { $('.form').submit(); });

    function setRoleDescription(roleitem) {
        var roles = {
            "3": "edit allow",
            "2": "editing not allowed ",
            "1": "only user info",
        };
        $('#role-description').html(roles[roleitem.val()]);
    }
});
