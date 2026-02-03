// ==================== ROLE SELECTION ====================

function selectRole(role) {
    // Hide role selection
    document.getElementById('roleSelection').style.display = 'none';

    // Show appropriate auth form
    if (role === 'student') {
        document.getElementById('studentAuth').style.display = 'block';
    } else if (role === 'worker') {
        document.getElementById('workerAuth').style.display = 'block';
    }
}

function backToRoleSelection() {
    // Hide auth forms
    document.getElementById('studentAuth').style.display = 'none';
    document.getElementById('workerAuth').style.display = 'none';

    // Show role selection
    document.getElementById('roleSelection').style.display = 'block';
}

// ==================== TAB SWITCHING ====================

function switchTab(tabId) {
    // Get all tabs and forms
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = {
        'student-login': document.getElementById('student-login'),
        'student-signup': document.getElementById('student-signup'),
        'worker-login': document.getElementById('worker-login'),
        'worker-signup': document.getElementById('worker-signup')
    };

    // Remove active class from all tabs
    tabs.forEach(tab => tab.classList.remove('active'));

    // Hide all forms
    Object.values(forms).forEach(form => {
        if (form) form.style.display = 'none';
    });

    // Activate clicked tab and show corresponding form
    event.target.classList.add('active');
    if (forms[tabId]) {
        forms[tabId].style.display = 'block';
    }
}

// ==================== PASSWORD TOGGLE ====================

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = event.target.closest('button').querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ==================== FORM VALIDATION ====================

// Student signup form validation
const studentSignupForm = document.getElementById('student-signup');
if (studentSignupForm) {
    studentSignupForm.addEventListener('submit', function (e) {
        const password = document.getElementById('student-signup-password').value;
        const confirmPassword = document.getElementById('student-signup-confirm').value;

        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Passwords do not match!');
            return false;
        }

        if (password.length < 6) {
            e.preventDefault();
            alert('Password must be at least 6 characters long!');
            return false;
        }

        return true;
    });
}

// Worker signup form validation
const workerSignupForm = document.getElementById('worker-signup');
if (workerSignupForm) {
    workerSignupForm.addEventListener('submit', function (e) {
        const password = document.getElementById('worker-signup-password').value;
        const confirmPassword = document.getElementById('worker-signup-confirm').value;

        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Passwords do not match!');
            return false;
        }

        if (password.length < 6) {
            e.preventDefault();
            alert('Password must be at least 6 characters long!');
            return false;
        }

        return true;
    });
}

// ==================== URL PARAMETERS ====================

// Check if role is specified in URL
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const role = urlParams.get('role');

    if (role === 'student' || role === 'worker') {
        selectRole(role);
    }

    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// ==================== FORM INPUT ENHANCEMENTS ====================

// Phone number formatting (student)
const phoneInput = document.getElementById('student-signup-phone');
if (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '').slice(0, 10);
    });
}

// Phone number formatting (worker)
const workerPhoneInput = document.getElementById('worker-signup-phone');
if (workerPhoneInput) {
    workerPhoneInput.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '').slice(0, 10);
    });
}

// Roll number uppercase
const rollInput = document.getElementById('student-signup-roll');
if (rollInput) {
    rollInput.addEventListener('input', function (e) {
        this.value = this.value.toUpperCase();
    });
}

// Employee ID uppercase
const empIdInput = document.getElementById('worker-signup-empid');
if (empIdInput) {
    empIdInput.addEventListener('input', function (e) {
        this.value = this.value.toUpperCase();
    });
}
