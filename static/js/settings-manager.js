function settingsManager() {
    return {
        isLoading: false,
        isImporting: false,
        activeTab: 'general',
        settings: {
            theme: 'light',
            language: 'en',
            timezone: 'UTC',
            dashboard_layout: 'grid',
            items_per_page: 20,
            email_notifications: true,
            push_notifications: true,
            import_completion_notifications: true,
            export_completion_notifications: true,
            error_notifications: true,
            enable_analytics: true,
            enable_bulk_operations: true,
            enable_progress_tracking: true,
            enable_export_history: true,
            enable_data_quality_reports: true,
            default_import_format: 'csv',
            default_export_format: 'csv',
            auto_delete_temp_files: true,
            temp_file_retention_days: 7,
            two_factor_enabled: false,
            session_timeout_minutes: 480,
            data_retention_days: 365,
            allow_data_sharing: false,
            allow_analytics_tracking: true
        },
        featureToggles: [],
        selectedFile: null,

        init() {
            this.loadSettings();
        },

        async loadSettings() {
            this.isLoading = true;
            try {
                const response = await fetch('/settings/api/get-settings/');
                const data = await response.json();
                
                if (data.success) {
                    this.settings = data.settings;
                    this.featureToggles = data.feature_toggles;
                } else {
                    console.error('Error loading settings:', data.error);
                    this.showNotification('Failed to load settings', 'error');
                }
            } catch (error) {
                console.error('Network error loading settings:', error);
                this.showNotification('Network error loading settings', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        async saveSettings() {
            try {
                const response = await fetch('/settings/api/update/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.settings)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.showNotification('Settings saved successfully', 'success');
                } else {
                    console.error('Error saving settings:', data.error);
                    this.showNotification('Failed to save settings', 'error');
                }
            } catch (error) {
                console.error('Network error saving settings:', error);
                this.showNotification('Network error saving settings', 'error');
            }
        },

        async saveAllSettings() {
            await this.saveSettings();
        },

        async toggleFeature(featureId) {
            try {
                const response = await fetch(`/settings/api/toggle-feature/${featureId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.showNotification(data.message, 'success');
                    // Update the feature toggle in our local data
                    const feature = this.featureToggles.find(f => f.id === featureId);
                    if (feature) {
                        feature.is_enabled = data.is_enabled;
                    }
                } else {
                    console.error('Error toggling feature:', data.error);
                    this.showNotification(data.error || 'Failed to toggle feature', 'error');
                }
            } catch (error) {
                console.error('Network error toggling feature:', error);
                this.showNotification('Network error toggling feature', 'error');
            }
        },

        async resetSettings() {
            if (!confirm('Are you sure you want to reset all settings to defaults? This action cannot be undone.')) {
                return;
            }

            try {
                const response = await fetch('/settings/reset/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    this.showNotification('Settings reset to defaults successfully', 'success');
                    this.loadSettings();
                } else {
                    this.showNotification('Failed to reset settings', 'error');
                }
            } catch (error) {
                console.error('Error resetting settings:', error);
                this.showNotification('Network error resetting settings', 'error');
            }
        },

        async exportSettings() {
            try {
                const response = await fetch('/settings/export/');
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `settings_${new Date().toISOString().split('T')[0]}.json`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    this.showNotification('Settings exported successfully', 'success');
                } else {
                    this.showNotification('Failed to export settings', 'error');
                }
            } catch (error) {
                console.error('Error exporting settings:', error);
                this.showNotification('Network error exporting settings', 'error');
            }
        },

        showImportModal() {
            const modal = new CustomModal(document.getElementById('importSettingsModal'));
            modal.show();
        },

        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file && file.type === 'application/json') {
                this.selectedFile = file;
            } else {
                this.showNotification('Please select a valid JSON file', 'error');
                event.target.value = '';
            }
        },

        async importSettings() {
            if (!this.selectedFile) {
                this.showNotification('Please select a file to import', 'error');
                return;
            }

            this.isImporting = true;
            try {
                const formData = new FormData();
                formData.append('settings_file', this.selectedFile);
                
                const response = await fetch('/settings/import/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.showNotification(data.message, 'success');
                    
                    // Close modal
                    const modalElement = document.getElementById('importSettingsModal');
                    if (modalElement) {
                        const modal = new CustomModal(modalElement);
                        modal.hide();
                    }
                    
                    // Reload settings
                    this.loadSettings();
                } else {
                    this.showNotification(data.error || 'Failed to import settings', 'error');
                }
            } catch (error) {
                console.error('Error importing settings:', error);
                this.showNotification('Network error importing settings', 'error');
            } finally {
                this.isImporting = false;
            }
        },

        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

            notification.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        },

        getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                   document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        }
    };
}
