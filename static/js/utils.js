/**
 * Utility Functions for Contact Manager
 * Common helper functions used across the application
 */

// Date and Time Utilities
const DateUtils = {
    formatDate(date, format = 'short') {
        if (!date) return '-';
        
        const d = new Date(date);
        const options = {
            'short': { year: 'numeric', month: 'short', day: 'numeric' },
            'long': { year: 'numeric', month: 'long', day: 'numeric' },
            'time': { hour: '2-digit', minute: '2-digit' },
            'datetime': { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
        };
        
        return d.toLocaleDateString('en-US', options[format] || options['short']);
    },
    
    formatRelativeTime(date) {
        if (!date) return '-';
        
        const now = new Date();
        const d = new Date(date);
        const diffInSeconds = Math.floor((now - d) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`;
        
        return this.formatDate(date);
    },
    
    formatDuration(milliseconds) {
        if (!milliseconds) return '-';
        
        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds % 60}s`;
        } else {
            return `${seconds}s`;
        }
    }
};

// File Utilities
const FileUtils = {
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    getFileExtension(filename) {
        return filename.split('.').pop().toLowerCase();
    },
    
    isValidFileType(filename, allowedTypes) {
        const extension = this.getFileExtension(filename);
        return allowedTypes.includes(extension);
    },
    
    downloadFile(url, filename) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};

// String Utilities
const StringUtils = {
    truncate(str, length = 50, suffix = '...') {
        if (!str || str.length <= length) return str;
        return str.substring(0, length) + suffix;
    },
    
    capitalize(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },
    
    slugify(str) {
        if (!str) return '';
        return str
            .toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, '-')
            .replace(/^-+|-+$/g, '');
    },
    
    highlightSearchTerm(text, searchTerm) {
        if (!searchTerm) return text;
        
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
};

// Number Utilities
const NumberUtils = {
    formatNumber(num, decimals = 0) {
        if (num === null || num === undefined) return '-';
        return num.toLocaleString('en-US', { 
            minimumFractionDigits: decimals, 
            maximumFractionDigits: decimals 
        });
    },
    
    formatCurrency(amount, currency = 'USD') {
        if (amount === null || amount === undefined) return '-';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    formatPercentage(value, decimals = 1) {
        if (value === null || value === undefined) return '-';
        return `${(value * 100).toFixed(decimals)}%`;
    }
};

// Validation Utilities
const ValidationUtils = {
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    isValidPhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    },
    
    isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    },
    
    isValidCSV(content) {
        // Basic CSV validation
        const lines = content.split('\n');
        if (lines.length < 2) return false;
        
        const firstLine = lines[0];
        const commaCount = (firstLine.match(/,/g) || []).length;
        
        // Check if all lines have similar comma count
        return lines.slice(1, 10).every(line => {
            const lineCommaCount = (line.match(/,/g) || []).length;
            return Math.abs(lineCommaCount - commaCount) <= 1;
        });
    }
};

// API Utilities
const ApiUtils = {
    async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    },
    
    async uploadFile(url, file, onProgress = null) {
        const formData = new FormData();
        formData.append('file', file);
        
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            if (onProgress) {
                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        const percentComplete = (e.loaded / e.total) * 100;
                        onProgress(percentComplete);
                    }
                });
            }
            
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        resolve(response);
                    } catch {
                        resolve(xhr.responseText);
                    }
                } else {
                    reject(new Error(`Upload failed: ${xhr.status}`));
                }
            });
            
            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });
            
            xhr.open('POST', url);
            xhr.setRequestHeader('X-CSRFToken', this.getCSRFToken());
            xhr.send(formData);
        });
    }
};

// UI Utilities
const UIUtils = {
    showToast(message, type = 'info', duration = 5000) {
        // This would integrate with the toast notification component
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('toast').show(message, type, duration);
        } else {
            // Fallback to browser alert
            alert(message);
        }
    },
    
    showLoading(message = 'Loading...') {
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('loading').show(message);
        }
    },
    
    hideLoading() {
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('loading').hide();
        }
    },
    
    showModal(title, content, size = 'normal') {
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('modal').show(title, content, size);
        }
    },
    
    hideModal() {
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('modal').hide();
        }
    },
    
    copyToClipboard(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    },
    
    scrollToElement(element, offset = 0) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (element) {
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    }
};

// Export utilities for global use
window.ContactManagerUtils = {
    DateUtils,
    FileUtils,
    StringUtils,
    NumberUtils,
    ValidationUtils,
    ApiUtils,
    UIUtils
};
