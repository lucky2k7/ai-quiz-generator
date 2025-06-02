// Form submission with loading state
document.getElementById('loginForm').addEventListener('submit', function(e) {
    const button = document.getElementById('loginButton');
    button.classList.add('btn-loading');
    button.textContent = '';
});

// Social login functionality (placeholder)
function socialLogin(provider) {
    console.log(`Initiating ${provider} login...`);
    // In a real Django app, this would redirect to social auth URLs
    // For example: window.location.href = `/auth/${provider}/`;
}

// Show error message function (for Django integration)
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Input focus animations
document.querySelectorAll('.form-group input').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.parentElement.style.transform = 'translateY(-2px)';
    });

    input.addEventListener('blur', function() {
        this.parentElement.parentElement.style.transform = 'translateY(0)';
    });
});

// Auto-hide error message when user starts typing
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', function() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv.style.display !== 'none') {
            errorDiv.style.display = 'none';
        }
    });
});