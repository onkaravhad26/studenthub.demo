// ==================== FILE UPLOAD HANDLING ====================

document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function () {
        const fileNameSpan = this.parentElement.querySelector('.file-name');
        if (this.files && this.files[0]) {
            fileNameSpan.textContent = this.files[0].name;
            fileNameSpan.classList.add('has-file');
        } else {
            fileNameSpan.textContent = 'No file chosen';
            fileNameSpan.classList.remove('has-file');
        }
    });
});

// ==================== FORM VALIDATION ====================

const applicationForm = document.getElementById('applicationForm');

if (applicationForm) {
    applicationForm.addEventListener('submit', function (e) {
        // Get all required file inputs
        const requiredFiles = this.querySelectorAll('input[type="file"][required]');
        let allFilesValid = true;

        requiredFiles.forEach(input => {
            if (!input.files || !input.files[0]) {
                allFilesValid = false;
                input.parentElement.querySelector('.file-input-label').style.borderColor = 'var(--danger-color)';
            }
        });

        if (!allFilesValid) {
            e.preventDefault();
            alert('Please upload all required documents!');
            return false;
        }

        // Check file sizes
        const allFileInputs = this.querySelectorAll('input[type="file"]');
        let fileSizeValid = true;

        allFileInputs.forEach(input => {
            if (input.files && input.files[0]) {
                const fileSizeMB = input.files[0].size / (1024 * 1024);
                const maxSize = input.id === 'photo' ? 1 : 2;

                if (fileSizeMB > maxSize) {
                    fileSizeValid = false;
                    alert(`File "${input.files[0].name}" exceeds maximum size of ${maxSize}MB`);
                }
            }
        });

        if (!fileSizeValid) {
            e.preventDefault();
            return false;
        }
    });
}

// ==================== AUTO-UPPERCASE FOR STATIONS ====================

const fromStation = document.getElementById('from_station');
const toStation = document.getElementById('to_station');

if (fromStation) {
    fromStation.addEventListener('input', function () {
        this.value = this.value.toUpperCase();
    });
}

if (toStation) {
    toStation.addEventListener('input', function () {
        this.value = this.value.toUpperCase();
    });
}

// ==================== AUTO-DISMISS FLASH MESSAGES ====================

setTimeout(function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (message) {
        message.style.animation = 'slideOutUp 0.3s ease';
        setTimeout(function () {
            message.remove();
        }, 300);
    });
}, 5000);
