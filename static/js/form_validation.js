document.addEventListener('DOMContentLoaded', function () {

    const passwordInput = document.getElementById('create_password');
    const passwordMessage = document.getElementById('create_password_message');

    const confirmPasswordInput = document.getElementById('confirm_password');
    const confirmPasswordMessage = document.getElementById('confirm_password_message');

    const lengthCheck = document.getElementById('length_check');
    const specialCheck = document.getElementById('special_check');
    const caseCheck = document.getElementById('case_check');

    const mobileInput = document.getElementById('mobile_number');
    const mobileMessage = document.getElementById('mobile_number_message');

    const digitCheck = document.getElementById('digit_check');
    const startCheck = document.getElementById('start_check');

    function validatePassword() {
        const password = passwordInput.value.trim();

        const hasLength = password.length >= 8;
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const hasUpper = /[A-Z]/.test(password);
        const hasLower = /[a-z]/.test(password);
        const hasCase = hasUpper && hasLower;

        lengthCheck.innerHTML = hasLength ? '<span style="color:green;">✓</span> Password must be at least 8 characters long.' : 'Password must be at least 8 characters long.';
        specialCheck.innerHTML = hasSpecial ? '<span style="color:green;">✓</span> Password must contain at least one special character.' : 'Password must contain at least one special character.';
        caseCheck.innerHTML = hasCase ? '<span style="color:green;">✓</span> Password must contain both uppercase and lowercase letters.' : 'Password must contain both uppercase and lowercase letters.';

        if (hasLength && hasSpecial && hasCase) {
            passwordMessage.innerHTML = '<span style="color: green;">✓</span> Password accepted';
        } else {
            passwordMessage.textContent = "";
        }
    }

    function validateConfirmPassword() {
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        if (password && confirmPassword && password === confirmPassword) {
            confirmPasswordMessage.innerHTML = '<span style="color: green;">✓</span> Password matched';
        } else {
            confirmPasswordMessage.textContent = "";
        }
    }

    function validateMobileNumber() {
        const mobile = mobileInput.value.trim();

        const hasTenDigits = /^\d{10}$/.test(mobile);
        const startsCorrectly = /^[6-9]/.test(mobile);

        digitCheck.innerHTML = hasTenDigits ? '<span style="color:green;">✓</span> Must be exactly 10 digits' : 'Must be exactly 10 digits';
        startCheck.innerHTML = startsCorrectly ? '<span style="color:green;">✓</span> Must start with 6, 7, 8, or 9' : 'Must start with 6, 7, 8, or 9';

        mobileMessage.innerHTML = (hasTenDigits && startsCorrectly) ? '<span style="color:green;">✓</span> Valid mobile number' : '';
    }

    if (passwordInput && confirmPasswordInput) {
        passwordInput.addEventListener('input', function () {
            validatePassword();
            validateConfirmPassword();
        });

        confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    }

    if (mobileInput) {
        mobileInput.addEventListener('input', validateMobileNumber);
    }

});
