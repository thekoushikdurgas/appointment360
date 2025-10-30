function exportHistory() {
    return {
        isLoading: false,
        isDeleting: false,
        isCreating: false,
        exports: [],
        selectedExports: [],
        stats: {
            total_exports: 0,
            completed_exports: 0,
            failed_exports: 0,
            total_records_exported: 0,
            total_file_size: 0,
            success_rate: 0
        },
        filters: {
            type: '',
            status: '',
            search: ''
        },
        newExport: {
            type: '',
            format: 'csv',
            filters: ''
        },
        currentPage: 1,
        totalPages: 1,
        pollingInterval: null,

        init() {
            this.loadExports();
            this.loadStats();
            this.startPolling();
        },

        async loadExports() {
            this.isLoading = true;
            try {
                const params = new URLSearchParams({
                    page: this.currentPage,
                    ...this.filters
                });
                
                const response = await fetch(`/exports/history/?${params}`);
                const html = await response.text();
                
                // Parse the HTML to extract exports data
                // This is a simplified approach - in a real app, you'd use an API
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Extract exports from the page
                this.extractExportsFromPage(doc);
                
            } catch (error) {
                console.error('Error loading exports:', error);
                this.showNotification('Failed to load exports', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        extractExportsFromPage(doc) {
            // This is a placeholder - you'd need to implement proper data extraction
            // For now, we'll use mock data
            this.exports = [
                {
                    id: 1,
                    export_type: 'contacts',
                    export_format: 'csv',
                    status: 'completed',
                    record_count: 1500,
                    file_size: 2048000,
                    created_at: new Date().toISOString(),
                    duration: '2m 30s',
                    progress_percentage: 100
                },
                {
                    id: 2,
                    export_type: 'bulk_export',
                    export_format: 'excel',
                    status: 'processing',
                    record_count: 0,
                    file_size: 0,
                    created_at: new Date(Date.now() - 300000).toISOString(),
                    duration: null,
                    progress_percentage: 45
                }
            ];
        },

        async loadStats() {
            try {
                const response = await fetch('/exports/api/stats/');
                const data = await response.json();
                
                if (data.error) {
                    console.error('Error loading stats:', data.error);
                    return;
                }
                
                this.stats = data.stats;
            } catch (error) {
                console.error('Network error loading stats:', error);
            }
        },

        async refreshExports() {
            await this.loadExports();
            await this.loadStats();
            this.showNotification('Exports refreshed successfully', 'success');
        },

        applyFilters() {
            this.currentPage = 1;
            this.loadExports();
        },

        // Selection management
        toggleExportSelection(exportId) {
            const index = this.selectedExports.indexOf(exportId);
            if (index > -1) {
                this.selectedExports.splice(index, 1);
            } else {
                this.selectedExports.push(exportId);
            }
        },

        isExportSelected(exportId) {
            return this.selectedExports.includes(exportId);
        },

        toggleAllExports() {
            if (this.allExportsSelected) {
                this.selectedExports = [];
            } else {
                this.selectedExports = this.exports.map(export => export.id);
            }
        },

        get allExportsSelected() {
            return this.exports.length > 0 && this.selectedExports.length === this.exports.length;
        },

        get someExportsSelected() {
            return this.selectedExports.length > 0 && this.selectedExports.length < this.exports.length;
        },

        clearSelection() {
            this.selectedExports = [];
        },

        // Export actions
        async downloadExport(exportId) {
            try {
                window.open(`/exports/api/download/${exportId}/`, '_blank');
                this.showNotification('Download started', 'success');
            } catch (error) {
                console.error('Error downloading export:', error);
                this.showNotification('Failed to download export', 'error');
            }
        },

        async cancelExport(exportId) {
            if (!confirm('Are you sure you want to cancel this export?')) {
                return;
            }

            try {
                const response = await fetch(`/exports/api/cancel/${exportId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    this.showNotification(data.message, 'success');
                    this.loadExports();
                } else {
                    this.showNotification(data.error || 'Failed to cancel export', 'error');
                }
            } catch (error) {
                console.error('Error cancelling export:', error);
                this.showNotification('Failed to cancel export', 'error');
            }
        },

        async deleteExport(exportId) {
            if (!confirm('Are you sure you want to delete this export?')) {
                return;
            }

            try {
                const response = await fetch(`/exports/api/delete/${exportId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    this.showNotification(data.message, 'success');
                    this.loadExports();
                    this.loadStats();
                } else {
                    this.showNotification(data.error || 'Failed to delete export', 'error');
                }
            } catch (error) {
                console.error('Error deleting export:', error);
                this.showNotification('Failed to delete export', 'error');
            }
        },

        async bulkDeleteExports() {
            if (!confirm(`Are you sure you want to delete ${this.selectedExports.length} export(s)?`)) {
                return;
            }

            this.isDeleting = true;
            try {
                const response = await fetch('/exports/api/bulk-delete/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        export_ids: this.selectedExports
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    this.showNotification(data.message, 'success');
                    this.clearSelection();
                    this.loadExports();
                    this.loadStats();
                } else {
                    this.showNotification(data.error || 'Failed to delete exports', 'error');
                }
            } catch (error) {
                console.error('Error bulk deleting exports:', error);
                this.showNotification('Failed to delete exports', 'error');
            } finally {
                this.isDeleting = false;
            }
        },

        // Create export modal
        showCreateExportModal() {
            const modal = new CustomModal(document.getElementById('createExportModal'));
            modal.show();
        },

        async createExport() {
            if (!this.newExport.type) {
                this.showNotification('Please select an export type', 'error');
                return;
            }

            this.isCreating = true;
            try {
                const filters = this.newExport.filters ? JSON.parse(this.newExport.filters) : {};
                
                const response = await fetch('/exports/api/create/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        export_type: this.newExport.type,
                        export_format: this.newExport.format,
                        filters: filters
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    this.showNotification(data.message, 'success');
                    this.newExport = { type: '', format: 'csv', filters: '' };
                    
                    // Close modal
                    const modalElement = document.getElementById('createExportModal');
                    if (modalElement) {
                        const modal = new CustomModal(modalElement);
                        modal.hide();
                    }
                    
                    this.loadExports();
                    this.loadStats();
                } else {
                    this.showNotification(data.error || 'Failed to create export', 'error');
                }
            } catch (error) {
                console.error('Error creating export:', error);
                this.showNotification('Failed to create export', 'error');
            } finally {
                this.isCreating = false;
            }
        },

        // Polling for real-time updates
        startPolling() {
            this.stopPolling();
            this.pollingInterval = setInterval(() => {
                this.loadExports();
            }, 5000); // Poll every 5 seconds
        },

        stopPolling() {
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
                this.pollingInterval = null;
            }
        },

        // Pagination
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.loadExports();
            }
        },

        getPageNumbers() {
            const pages = [];
            const start = Math.max(1, this.currentPage - 2);
            const end = Math.min(this.totalPages, this.currentPage + 2);
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            
            return pages;
        },

        // Utility functions
        formatFileSize(bytes) {
            if (!bytes) return '0 B';
            
            const units = ['B', 'KB', 'MB', 'GB', 'TB'];
            let size = bytes;
            let unitIndex = 0;
            
            while (size >= 1024 && unitIndex < units.length - 1) {
                size /= 1024;
                unitIndex++;
            }
            
            return `${size.toFixed(1)} ${units[unitIndex]}`;
        },

        formatDate(dateString) {
            if (!dateString) return '-';
            const date = new Date(dateString);
            return date.toLocaleString();
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
