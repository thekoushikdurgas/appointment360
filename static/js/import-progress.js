// Import progress polling and cancel support
(function () {
  function fetchStatus(jobId, onUpdate) {
    fetch(`/imports/api/job/${jobId}/status/`, { headers: { 'Accept': 'application/json' } })
      .then(r => r.json())
      .then(data => onUpdate && onUpdate(data))
      .catch(() => {});
  }

  function cancelJob(jobId, onDone) {
    fetch(`/imports/api/job/${jobId}/cancel/`, {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    }).then(r => r.json()).then(onDone).catch(() => {});
  }

  window.progressTracker = function(jobId) {
    return {
      jobId: jobId,
      jobData: {
        status: 'PENDING',
        progress_percentage: 0,
        processed_rows: 0,
        total_rows: 0,
        success_count: 0,
        error_count: 0,
        duplicate_count: 0,
        processing_speed: 0,
        current_batch: 0,
        total_batches: 0,
        started_at: null,
        completed_at: null,
        estimated_completion: null,
        duration: null,
        error_log: null
      },
      isCancelling: false,
      recentJobs: [],
      intervalId: null,
      init() {
        if (this.jobId) {
          this.startPolling();
        } else {
          this.fetchRecentJobs();
        }
      },
      startPolling() {
        const update = () => {
          fetchStatus(this.jobId, (data) => {
            if (data && !data.error) {
              this.jobData = data;
              if (data.is_complete) {
                this.stopPolling();
              }
            }
          });
        };
        update();
        this.intervalId = setInterval(update, 2000);
      },
      stopPolling() {
        if (this.intervalId) clearInterval(this.intervalId);
        this.intervalId = null;
      },
      cancelJob() {
        if (!this.jobId || this.isCancelling) return;
        this.isCancelling = true;
        cancelJob(this.jobId, () => {
          this.isCancelling = false;
          this.stopPolling();
          this.startPolling();
        });
      },
      formatETA(iso) {
        try {
          const d = new Date(iso);
          return d.toLocaleString();
        } catch (e) { return ''; }
      },
      fetchRecentJobs() {
        fetch('/imports/api/recent-jobs/')
          .then(r => r.json())
          .then(data => { this.recentJobs = data.jobs || []; })
          .catch(() => {});
      }
    }
  }
})();

/**
 * Import Progress Tracker - Alpine.js Component
 * Real-time progress monitoring for CSV import jobs
 */

function progressTracker(jobId) {
    return {
        jobId: jobId,
        jobData: {
            id: jobId,
            status: 'PENDING',
            progress_percentage: 0,
            total_rows: 0,
            processed_rows: 0,
            success_count: 0,
            error_count: 0,
            duplicate_count: 0,
            processing_speed: 0,
            current_batch: 0,
            total_batches: 0,
            estimated_completion: null,
            started_at: null,
            completed_at: null,
            duration: null,
            error_log: null
        },
        recentJobs: [],
        isCancelling: false,
        pollingInterval: null,
        websocket: null,
        lastUpdate: null,

        init() {
            console.log('Initializing progress tracker for job:', this.jobId);
            
            // Load initial data
            this.loadJobData();
            
            // Setup real-time updates
            this.setupRealTimeUpdates();
            
            // Load recent jobs if no specific job
            if (!this.jobId) {
                this.loadRecentJobs();
            }
        },

        async loadJobData() {
            try {
                const response = await fetch(`/api/imports/job/${this.jobId}/status/`);
                if (response.ok) {
                    const data = await response.json();
                    this.updateJobData(data);
                } else {
                    console.error('Failed to load job data:', response.statusText);
                    this.showNotification('Failed to load job data', 'error');
                }
            } catch (error) {
                console.error('Error loading job data:', error);
                this.showNotification('Error loading job data', 'error');
            }
        },

        async loadRecentJobs() {
            try {
                const response = await fetch('/api/imports/recent-jobs/');
                if (response.ok) {
                    const data = await response.json();
                    this.recentJobs = data.jobs || [];
                }
            } catch (error) {
                console.error('Error loading recent jobs:', error);
            }
        },

        setupRealTimeUpdates() {
            if (!this.jobId) return;

            // Try WebSocket first
            this.setupWebSocket();
            
            // Fallback to AJAX polling
            this.setupPolling();
        },

        setupWebSocket() {
            try {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/import/${this.jobId}/`;
                
                this.websocket = new WebSocket(wsUrl);
                
                this.websocket.onopen = () => {
                    console.log('WebSocket connected');
                };
                
                this.websocket.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.handleProgressUpdate(data);
                    } catch (error) {
                        console.error('Error parsing WebSocket message:', error);
                    }
                };
                
                this.websocket.onclose = () => {
                    console.log('WebSocket disconnected, falling back to polling');
                    this.setupPolling();
                };
                
                this.websocket.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    this.setupPolling();
                };
            } catch (error) {
                console.error('WebSocket setup failed:', error);
                this.setupPolling();
            }
        },

        setupPolling() {
            // Stop existing polling
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
            }

            // Start polling every 2 seconds
            this.pollingInterval = setInterval(() => {
                this.pollForUpdates();
            }, 2000);

            console.log('Started AJAX polling for job updates');
        },

        async pollForUpdates() {
            try {
                const response = await fetch(`/api/imports/job/${this.jobId}/status/`);
                if (response.ok) {
                    const data = await response.json();
                    this.handleProgressUpdate(data);
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        },

        handleProgressUpdate(data) {
            // Avoid duplicate updates
            if (this.lastUpdate && this.lastUpdate === data.last_updated) {
                return;
            }
            
            this.lastUpdate = data.last_updated;
            this.updateJobData(data);
            
            // Stop polling if job is complete
            if (data.status === 'COMPLETED' || data.status === 'FAILED' || data.status === 'CANCELLED') {
                this.stopPolling();
                this.showCompletionNotification(data.status);
            }
        },

        updateJobData(data) {
            // Animate counter changes
            this.animateCounter('total_rows', data.total_rows);
            this.animateCounter('processed_rows', data.processed_rows);
            this.animateCounter('success_count', data.success_count);
            this.animateCounter('error_count', data.error_count);
            this.animateCounter('duplicate_count', data.duplicate_count);
            
            // Update other fields
            this.jobData.status = data.status;
            this.jobData.progress_percentage = data.progress_percentage || 0;
            this.jobData.processing_speed = data.processing_speed || 0;
            this.jobData.current_batch = data.current_batch || 0;
            this.jobData.total_batches = data.total_batches || 0;
            this.jobData.estimated_completion = data.estimated_completion;
            this.jobData.started_at = data.started_at;
            this.jobData.completed_at = data.completed_at;
            this.jobData.duration = data.duration;
            this.jobData.error_log = data.error_log;
        },

        animateCounter(field, newValue) {
            const currentValue = this.jobData[field] || 0;
            if (currentValue !== newValue) {
                // Simple animation - could be enhanced with easing
                this.jobData[field] = newValue;
            }
        },

        async cancelJob() {
            if (!confirm('Are you sure you want to cancel this import job?')) {
                return;
            }

            this.isCancelling = true;
            
            try {
                const response = await fetch(`/api/imports/job/${this.jobId}/cancel/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    }
                });

                if (response.ok) {
                    this.showNotification('Job cancelled successfully', 'success');
                    // Refresh data to show updated status
                    setTimeout(() => this.loadJobData(), 1000);
                } else {
                    const error = await response.json();
                    this.showNotification(error.message || 'Failed to cancel job', 'error');
                }
            } catch (error) {
                console.error('Error cancelling job:', error);
                this.showNotification('Error cancelling job', 'error');
            } finally {
                this.isCancelling = false;
            }
        },

        stopPolling() {
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
                this.pollingInterval = null;
            }
            
            if (this.websocket) {
                this.websocket.close();
                this.websocket = null;
            }
        },

        formatETA(etaString) {
            if (!etaString) return 'Calculating...';
            
            try {
                const eta = new Date(etaString);
                const now = new Date();
                const diff = eta - now;
                
                if (diff <= 0) return 'Soon';
                
                const minutes = Math.floor(diff / 60000);
                const seconds = Math.floor((diff % 60000) / 1000);
                
                if (minutes > 0) {
                    return `${minutes}m ${seconds}s`;
                } else {
                    return `${seconds}s`;
                }
            } catch (error) {
                return 'Calculating...';
            }
        },

        showCompletionNotification(status) {
            const messages = {
                'COMPLETED': 'Import completed successfully!',
                'FAILED': 'Import failed. Check the error details.',
                'CANCELLED': 'Import was cancelled.'
            };
            
            const types = {
                'COMPLETED': 'success',
                'FAILED': 'error',
                'CANCELLED': 'warning'
            };
            
            this.showNotification(messages[status], types[status]);
        },

        showNotification(message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            
            notification.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(notification);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        },

        getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                   document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        },

        // Cleanup on component destroy
        destroy() {
            this.stopPolling();
        }
    };
}

// Global utility functions
window.ProgressTracker = {
    // Initialize progress tracker for any element
    init(element, jobId) {
        if (typeof Alpine !== 'undefined') {
            Alpine.data('progressTracker', () => progressTracker(jobId));
        }
    },
    
    // Show notification globally
    showNotification(message, type = 'info') {
        const tracker = new progressTracker(null);
        tracker.showNotification(message, type);
    }
};

// Auto-initialize if Alpine.js is available
document.addEventListener('DOMContentLoaded', function() {
    if (typeof Alpine !== 'undefined') {
        console.log('Progress tracker initialized with Alpine.js');
    } else {
        console.warn('Alpine.js not found. Progress tracker requires Alpine.js.');
    }
});
