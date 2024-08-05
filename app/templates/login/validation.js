<script>
    $(document).ready(function() {
        function validateField(field, regex, errorElement, errorMessage) {
            let value = $(field).val();
            if (!regex.test(value)) {
                $(errorElement).text(errorMessage);
                return false;
            } else {
                $(errorElement).text('');
                return true;
            }
        }

        function validateForm() {
            let isFullNameValid = validateField('#fullName', /^[a-zA-Z\s]+$/, '#fullNameError', 'Invalid full name');
            let isUsernameValid = validateField('#username', /^[a-zA-Z0-9_]+$/, '#usernameError', 'Invalid username');
            let isEmailValid = validateField('#email',/^[^\s@]+@gmail\.com$/,'#emailError','Invalid email address. Only gmail.com domain is allowed.');
            let isPhoneValid = validateField('#phone', /^[0-9]{10}$/, '#phoneError', 'Invalid phone number');
            let isAddressValid = validateField('#address', /.+/, '#addressError', 'Address cannot be empty');
            let isDobValid = validateField('#dob', /.+/, '#dobError', 'Date of birth cannot be empty');
            let isPasswordValid = validateField('#password', /.{6,}/, '#passwordError', 'Password must be at least 6 characters');
            let isConfirmPasswordValid = validateField('#confirmpassword', new RegExp(`^${$('#password').val()}$`), '#confirmpasswordError', 'Passwords do not match');

            let isFormValid = isFullNameValid && isUsernameValid && isEmailValid && isPhoneValid && isAddressValid && isDobValid && isPasswordValid && isConfirmPasswordValid;
            
            $('#submit').prop('disabled', !isFormValid);
        }

        $('input').on('input', function() {
            validateForm();
        });

        $('#registerForm').on('submit', function(e) {
            validateForm();
            if ($('#submit').prop('disabled')) {
                e.preventDefault();
            }
        });
    });
</script>