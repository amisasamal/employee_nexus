document.addEventListener('DOMContentLoaded', function () {
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');

    requiredFields.forEach(field => {
        const errorId = `${field.name}_error`;
        const errorSpan = document.getElementById(errorId);

        // Show error only on blur if field is empty
        field.addEventListener('blur', function () {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                if (errorSpan) {
                    errorSpan.textContent = `${field.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} is required`;
                }
            }
        });

        // Clear error while typing
        field.addEventListener('input', function () {
            if (field.value.trim()) {
                field.classList.remove('is-invalid');
                if (errorSpan) {
                    errorSpan.textContent = '';
                }
            }
        });
    });
});
