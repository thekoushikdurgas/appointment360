/**
 * Reusable Alpine.js Components Library
 * Collection of commonly used Alpine.js components for the Contact Manager application
 */

// Toast Notification Component
function toastNotification() {
    return {
        show: false,
        message: '',
        type: 'info', // info, success, warning, error
        duration: 5000,
        position: 'top-right', // top-right, top-left, bottom-right, bottom-left

        init() {
            // Auto-hide after duration
            if (this.show) {
                setTimeout(() => {
                    this.hide();
                }, this.duration);
            }
        },

        showToast(message, type = 'info', duration = 5000) {
            this.message = message;
            this.type = type;
            this.duration = duration;
            this.show = true;
            
            setTimeout(() => {
                this.hide();
            }, this.duration);
        },

        hide() {
            this.show = false;
        },

        getIconClass() {
            const icons = {
                'info': 'fas fa-info-circle',
                'success': 'fas fa-check-circle',
                'warning': 'fas fa-exclamation-triangle',
                'error': 'fas fa-exclamation-circle'
            };
            return icons[this.type] || icons['info'];
        },

        getAlertClass() {
            const classes = {
                'info': 'alert-info',
                'success': 'alert-success',
                'warning': 'alert-warning',
                'error': 'alert-danger'
            };
            return classes[this.type] || classes['info'];
        }
    };
}

// Loading Spinner Component
function loadingSpinner() {
    return {
        show: false,
        message: 'Loading...',
        size: 'normal', // small, normal, large
        overlay: false,

        showSpinner(message = 'Loading...', size = 'normal', overlay = false) {
            this.message = message;
            this.size = size;
            this.overlay = overlay;
            this.show = true;
        },

        hideSpinner() {
            this.show = false;
        },

        getSizeClass() {
            const sizes = {
                'small': 'spinner-border-sm',
                'normal': '',
                'large': 'spinner-border-lg'
            };
            return sizes[this.size] || sizes['normal'];
        }
    };
}

// Modal Component
function modalComponent() {
    return {
        show: false,
        title: '',
        content: '',
        size: 'normal', // small, normal, large, xl
        closable: true,
        backdrop: true,

        showModal(title, content, size = 'normal', closable = true, backdrop = true) {
            this.title = title;
            this.content = content;
            this.size = size;
            this.closable = closable;
            this.backdrop = backdrop;
            this.show = true;
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        },

        hideModal() {
            this.show = false;
            document.body.style.overflow = '';
        },

        getSizeClass() {
            const sizes = {
                'small': 'modal-sm',
                'normal': '',
                'large': 'modal-lg',
                'xl': 'modal-xl'
            };
            return sizes[this.size] || sizes['normal'];
        }
    };
}

// Form Validation Component
function formValidation() {
    return {
        errors: {},
        isValid: true,
        submitted: false,

        validateField(fieldName, value, rules = {}) {
            const errors = [];
            
            // Required validation
            if (rules.required && (!value || value.trim() === '')) {
                errors.push(`${fieldName} is required`);
            }
            
            // Email validation
            if (rules.email && value && !this.isValidEmail(value)) {
                errors.push(`${fieldName} must be a valid email address`);
            }
            
            // Min length validation
            if (rules.minLength && value && value.length < rules.minLength) {
                errors.push(`${fieldName} must be at least ${rules.minLength} characters`);
            }
            
            // Max length validation
            if (rules.maxLength && value && value.length > rules.maxLength) {
                errors.push(`${fieldName} must be no more than ${rules.maxLength} characters`);
            }
            
            // Pattern validation
            if (rules.pattern && value && !rules.pattern.test(value)) {
                errors.push(`${fieldName} format is invalid`);
            }
            
            if (errors.length > 0) {
                this.errors[fieldName] = errors;
                this.isValid = false;
            } else {
                delete this.errors[fieldName];
            }
            
            return errors.length === 0;
        },

        validateForm(formData, rules) {
            this.errors = {};
            this.isValid = true;
            
            for (const [fieldName, value] of Object.entries(formData)) {
                if (rules[fieldName]) {
                    this.validateField(fieldName, value, rules[fieldName]);
                }
            }
            
            return this.isValid;
        },

        isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },

        getFieldErrors(fieldName) {
            return this.errors[fieldName] || [];
        },

        hasFieldError(fieldName) {
            return fieldName in this.errors;
        },

        clearErrors() {
            this.errors = {};
            this.isValid = true;
            this.submitted = false;
        }
    };
}

// Data Table Component
function dataTable() {
    return {
        data: [],
        filteredData: [],
        searchTerm: '',
        sortField: '',
        sortDirection: 'asc',
        currentPage: 1,
        itemsPerPage: 10,
        selectedItems: [],
        loading: false,

        init() {
            this.filteredData = [...this.data];
        },

        setData(newData) {
            this.data = newData;
            this.filteredData = [...newData];
            this.currentPage = 1;
            this.selectedItems = [];
        },

        search() {
            if (!this.searchTerm) {
                this.filteredData = [...this.data];
            } else {
                this.filteredData = this.data.filter(item => {
                    return Object.values(item).some(value => 
                        String(value).toLowerCase().includes(this.searchTerm.toLowerCase())
                    );
                });
            }
            this.currentPage = 1;
        },

        sort(field) {
            if (this.sortField === field) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortField = field;
                this.sortDirection = 'asc';
            }
            
            this.filteredData.sort((a, b) => {
                const aVal = a[field];
                const bVal = b[field];
                
                if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });
        },

        getPaginatedData() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredData.slice(start, end);
        },

        getTotalPages() {
            return Math.ceil(this.filteredData.length / this.itemsPerPage);
        },

        goToPage(page) {
            if (page >= 1 && page <= this.getTotalPages()) {
                this.currentPage = page;
            }
        },

        selectItem(itemId) {
            const index = this.selectedItems.indexOf(itemId);
            if (index > -1) {
                this.selectedItems.splice(index, 1);
            } else {
                this.selectedItems.push(itemId);
            }
        },

        selectAll() {
            const pageData = this.getPaginatedData();
            this.selectedItems = pageData.map(item => item.id);
        },

        clearSelection() {
            this.selectedItems = [];
        },

        isSelected(itemId) {
            return this.selectedItems.includes(itemId);
        },

        get allSelected() {
            const pageData = this.getPaginatedData();
            return pageData.length > 0 && pageData.every(item => this.isSelected(item.id));
        },

        get someSelected() {
            const pageData = this.getPaginatedData();
            return pageData.some(item => this.isSelected(item.id));
        }
    };
}

// File Upload Component
function fileUpload() {
    return {
        files: [],
        maxFiles: 5,
        maxSize: 10 * 1024 * 1024, // 10MB
        allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
        dragOver: false,
        uploading: false,
        progress: 0,

        init() {
            // Set up drag and drop
            this.$el.addEventListener('dragover', (e) => {
                e.preventDefault();
                this.dragOver = true;
            });
            
            this.$el.addEventListener('dragleave', (e) => {
                e.preventDefault();
                this.dragOver = false;
            });
            
            this.$el.addEventListener('drop', (e) => {
                e.preventDefault();
                this.dragOver = false;
                this.handleFiles(e.dataTransfer.files);
            });
        },

        handleFiles(fileList) {
            for (let file of fileList) {
                if (this.validateFile(file)) {
                    this.files.push({
                        file: file,
                        id: Date.now() + Math.random(),
                        name: file.name,
                        size: file.size,
                        type: file.type,
                        status: 'pending'
                    });
                }
            }
        },

        validateFile(file) {
            // Check file type
            if (!this.allowedTypes.includes(file.type)) {
                this.showError(`File type ${file.type} is not allowed`);
                return false;
            }
            
            // Check file size
            if (file.size > this.maxSize) {
                this.showError(`File ${file.name} is too large. Maximum size is ${this.formatFileSize(this.maxSize)}`);
                return false;
            }
            
            // Check max files
            if (this.files.length >= this.maxFiles) {
                this.showError(`Maximum ${this.maxFiles} files allowed`);
                return false;
            }
            
            return true;
        },

        removeFile(fileId) {
            this.files = this.files.filter(f => f.id !== fileId);
        },

        async uploadFiles() {
            this.uploading = true;
            this.progress = 0;
            
            try {
                for (let i = 0; i < this.files.length; i++) {
                    const fileData = this.files[i];
                    fileData.status = 'uploading';
                    
                    // Simulate upload progress
                    for (let progress = 0; progress <= 100; progress += 10) {
                        fileData.progress = progress;
                        this.progress = ((i * 100) + progress) / this.files.length;
                        await new Promise(resolve => setTimeout(resolve, 100));
                    }
                    
                    fileData.status = 'completed';
                }
                
                this.showSuccess('Files uploaded successfully');
            } catch (error) {
                this.showError('Upload failed: ' + error.message);
            } finally {
                this.uploading = false;
            }
        },

        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        showError(message) {
            // This would integrate with the toast notification component
            console.error(message);
        },

        showSuccess(message) {
            // This would integrate with the toast notification component
            console.log(message);
        }
    };
}

// Progress Bar Component
function progressBar() {
    return {
        progress: 0,
        max: 100,
        show: false,
        message: '',
        animated: false,
        striped: false,

        showProgress(progress, message = '', animated = false, striped = false) {
            this.progress = Math.min(Math.max(progress, 0), this.max);
            this.message = message;
            this.animated = animated;
            this.striped = striped;
            this.show = true;
        },

        hideProgress() {
            this.show = false;
            this.progress = 0;
            this.message = '';
        },

        updateProgress(progress, message = '') {
            this.progress = Math.min(Math.max(progress, 0), this.max);
            if (message) this.message = message;
        },

        getProgressPercentage() {
            return (this.progress / this.max) * 100;
        },

        getProgressClass() {
            let classes = 'progress-bar';
            if (this.animated) classes += ' progress-bar-animated';
            if (this.striped) classes += ' progress-bar-striped';
            return classes;
        }
    };
}

// Export all components for global use
window.AlpineComponents = {
    toastNotification,
    loadingSpinner,
    modalComponent,
    formValidation,
    dataTable,
    fileUpload,
    progressBar
};
