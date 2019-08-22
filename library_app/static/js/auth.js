$(document).ready(function() {
    $('.ui.form').form({
        fields: {
            email: {
                identifier: 'email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your e-mail'
                    },
                    {
                        type: 'email',
                        prompt: 'Please enter a valid e-mail'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your password'
                    },
                    {
                        type: 'length[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }
                ]
            }
        }
    });
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#register-div').toggle();
    $('#login-link').click(function (event) {
        event.preventDefault();
        $('#register-div').fadeToggle();
        $('#login-div').fadeToggle();
    });
    $('#register-link').click(function (event) {
        event.preventDefault();
        $('#login-div').fadeToggle();
        $('#register-div').fadeToggle();
    });
});
