$(document).ready(function () {

    $("#show_hide_password button").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password input').attr("type") == "text"){
            $('#show_hide_password input').attr('type', 'password');
            $('#show_hide_password i').removeClass( "fa fa-sharp fa-solid fa-eye" );
            $('#show_hide_password i').addClass( "fa fa-solid fa-eye-slash" );
        }else if($('#show_hide_password input').attr("type") == "password"){
            $('#show_hide_password input').attr('type', 'text');
            $('#show_hide_password i').removeClass( "fa fa-solid fa-eye-slash" );
            $('#show_hide_password i').addClass( "fa fa-sharp fa-solid fa-eye" );
        }
    });
});