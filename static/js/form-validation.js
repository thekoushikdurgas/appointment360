// Form Validation JavaScript - Contact Manager

(function() {
    'use strict';
    
    const FormValidation = {
        init: function() {
            this.setupEmailValidation();
            this.setupPasswordStrength();
            this.setupCharacterCounters();
            this.setupRealTimeValidation();
            this.setupFormSubmission();
        },
        
        setupEmailValidation: function() {
            const emailFields = document.querySelectorAll('input[type="email"]');
            
            emailFields.forEach(field => {
                field.addEventListener('blur', function() {
                    FormValidation.validateEmail(this);
                });
                
                field.addEventListener('input', function() {
                    if (this.classList.contains('is-invalid')) {
                        FormValidation.validateEmail(this);
                    }
                });
            });
        },
        
        validateEmail: function(field) {
            const email = field.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email && !emailRegex.test(email)) {
                field.classList.add('is-invalid');
                field.classList.remove('is-valid');
                FormValidation.showFieldError(field, 'Please enter a valid email address');
            } else if (email) {
                field.classList.add('is-valid');
                field.classList.remove('is-invalid');
                FormValidation.hideFieldError(field);
            } else {
                field.classList.remove('is-valid', 'is-invalid');
                FormValidation.hideFieldError(field);
            }
        },
        
        setupPasswordStrength: function() {
            const passwordFields = document.querySelectorAll('input[type="password"]');
            
            passwordFields.forEach(field => {
                if (field.name === 'password') {
                    field.addEventListener('input', function() {
                        FormValidation.updatePasswordStrength(this);
                    });
                }
            });
        },
        
        updatePasswordStrength: function(field) {
            const password = field.value;
            const strengthBar = document.getElementById('strengthBar');
            
            if (!strengthBar) return;
            
            let strength = 0;
            let strengthClass = '';
            let color = '';
            
            if (password.length >= 8) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
            
            switch(strength) {
                case 0:
                    strengthClass = 'password-strength-weak';
                    color = '#dc3545';
                    break;
                case 1:
                case 2:
                    strengthClass = 'password-strength-fair';
                    color = '#ffc107';
                    break;
                case 3:
                case 4:
                    strengthClass = 'password-strength-good';
                    color = '#28a745';
                    break;
                case 5:
                    strengthClass = 'password-strength-strong';
                    color = '#20c997';
                    break;
            }
            
            strengthBar.style.width = `${(strength / 5) * 100}%`;
            strengthBar.className = `password-strength-bar ${strengthClass}`;
            strengthBar.style.backgroundColor = color;
        },
        
        setupCharacterCounters: function() {
            const textareas = document.querySelectorAll('textarea[maxlength]');
            
            textareas.forEach(textarea => {
                const maxLength = parseInt(textarea.getAttribute('maxlength'));
                if (isNaN(maxLength)) return;
                
                const counter = document.createElement('div');
                counter.className = 'char-counter';
                counter.id = `${textarea.id}-counter`;
                textarea.parentNode.appendChild(counter);
                
                function updateCounter() {
                    const length = textarea.value.length;
                    counter.textContent = `${length}/${maxLength} characters`;
                    
                    if (length > maxLength * 0.9) {
                        counter.classList.add('danger');
                    } else if (length > maxLength * 0.7) {
                        counter.classList.add('warning');
                    } else {
                        counter.classList.remove('danger', 'warning');
                    }
                }
                
                textarea.addEventListener('input', updateCounter);
                updateCounter();
            });
        },
        
        setupRealTimeValidation: function() {
            const requiredFields = document.querySelectorAll('input[required], textarea[required], select[required]');
            
            requiredFields.forEach(field => {
                field.addEventListener('blur', function() {
                    FormValidation.validateRequired(this);
                });
            });
        },
        
        validateRequired: function(field) {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                field.classList.remove('is-valid');
                FormValidation.showFieldError(field, 'This field is required');
            } else {
                field.classList.add('is-valid');
                field.classList.remove('is-invalid');
                FormValidation.hideFieldError(field);
            }
        },
        
        setupFormSubmission: function() {
            const forms = document.querySelectorAll('form');
            
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    if (!FormValidation.validateForm(this)) {
                        e.preventDefault();
                        FormValidation.showFormErrors(this);
                    }
                });
            });
        },
        
        validateForm: function(form) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('input[required], textarea[required], select[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Validate email fields
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                if (field.value && !FormValidation.isValidEmail(field.value)) {
                    field.classList.add('is-invalid');
                    isValid = false;
                }
            });
            
            return isValid;
        },
        
        isValidEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
        
        showFieldError: function(field, message) {
            FormValidation.hideFieldError(field);
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback d-block';
            errorDiv.textContent = message;
            errorDiv.id = `${field.id}-error`;
            
            field.parentNode.appendChild(errorDiv);
        },
        
        hideFieldError: function(field) {
            const errorDiv = document.getElementById(`${field.id}-error`);
            if (errorDiv) {
                errorDiv.remove();
            }
        },
        
        showFormErrors: function(form) {
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
        }
    };
    
    // Export to global scope
    window.FormValidation = FormValidation;
    
    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        FormValidation.init();
    });
})();

