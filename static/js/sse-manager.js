/**
 * Server-Sent Events (SSE) Manager
 * Handles real-time updates from the server
 */
class SSEManager {
    constructor() {
        this.eventSource = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.isConnected = false;
        this.listeners = new Map();
        this.heartbeatTimeout = null;
    }

    connect() {
        if (this.eventSource && this.eventSource.readyState !== EventSource.CLOSED) {
            return;
        }

        try {
            this.eventSource = new EventSource('/sse/updates/');
            
            this.eventSource.onopen = (event) => {
                console.log('SSE connection opened');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.startHeartbeat();
                this.emit('connected', event);
            };

            this.eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Error parsing SSE message:', error);
                }
            };

            this.eventSource.onerror = (event) => {
                console.error('SSE connection error:', event);
                this.isConnected = false;
                this.stopHeartbeat();
                this.emit('error', event);
                
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.scheduleReconnect();
                } else {
                    console.error('Max reconnection attempts reached');
                    this.emit('max_reconnect_attempts');
                }
            };

        } catch (error) {
            console.error('Error creating SSE connection:', error);
            this.emit('error', error);
        }
    }

    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
        this.isConnected = false;
        this.stopHeartbeat();
    }

    scheduleReconnect() {
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`Scheduling reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);
        
        setTimeout(() => {
            this.connect();
        }, delay);
    }

    startHeartbeat() {
        this.heartbeatTimeout = setTimeout(() => {
            if (this.isConnected) {
                console.log('SSE heartbeat timeout - reconnecting');
                this.disconnect();
                this.connect();
            }
        }, 35000); // 35 seconds timeout
    }

    stopHeartbeat() {
        if (this.heartbeatTimeout) {
            clearTimeout(this.heartbeatTimeout);
            this.heartbeatTimeout = null;
        }
    }

    handleMessage(data) {
        const { type, data: messageData, timestamp } = data;
        
        // Reset heartbeat on any message
        this.startHeartbeat();
        
        switch (type) {
            case 'connected':
                console.log('SSE connected at', timestamp);
                break;
                
            case 'heartbeat':
                // Heartbeat received, connection is alive
                break;
                
            case 'import_update':
                this.handleImportUpdate(messageData);
                break;
                
            case 'export_update':
                this.handleExportUpdate(messageData);
                break;
                
            case 'contact_count_update':
                this.handleContactCountUpdate(messageData);
                break;
                
            case 'notification':
                this.handleNotification(messageData);
                break;
                
            case 'error':
                console.error('SSE server error:', messageData);
                break;
                
            default:
                console.log('Unknown SSE message type:', type, messageData);
        }
        
        // Emit generic message event
        this.emit('message', { type, data: messageData, timestamp });
    }

    handleImportUpdate(data) {
        // Update import progress components
        this.emit('import_update', data);
        
        // Update any progress bars
        const progressBars = document.querySelectorAll('[data-import-id="' + data.id + '"]');
        progressBars.forEach(bar => {
            const progressBar = bar.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = data.progress_percentage + '%';
                progressBar.setAttribute('aria-valuenow', data.progress_percentage);
            }
        });
        
        // Update status badges
        const statusBadges = document.querySelectorAll('[data-import-status-id="' + data.id + '"]');
        statusBadges.forEach(badge => {
            badge.textContent = data.status;
            badge.className = `badge bg-${this.getStatusColor(data.status)}`;
        });
        
        // Show completion notification
        if (data.is_complete) {
            this.showNotification(
                `Import completed: ${data.success_count} contacts imported successfully`,
                'success'
            );
        }
        
        // Show error notification
        if (data.is_failed && data.error_log) {
            this.showNotification(
                `Import failed: ${data.error_log}`,
                'error'
            );
        }
    }

    handleExportUpdate(data) {
        // Update export status components
        this.emit('export_update', data);
        
        // Update export progress
        const exportCards = document.querySelectorAll('[data-export-id="' + data.id + '"]');
        exportCards.forEach(card => {
            const statusBadge = card.querySelector('.export-status');
            if (statusBadge) {
                statusBadge.textContent = data.status;
                statusBadge.className = `badge bg-${this.getStatusColor(data.status)}`;
            }
            
            const progressBar = card.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = data.progress_percentage + '%';
            }
        });
        
        // Show completion notification
        if (data.is_completed) {
            this.showNotification(
                `Export completed: ${data.filename} ready for download`,
                'success'
            );
        }
        
        // Show error notification
        if (data.is_failed && data.error_message) {
            this.showNotification(
                `Export failed: ${data.error_message}`,
                'error'
            );
        }
    }

    handleContactCountUpdate(data) {
        // Update contact count displays
        this.emit('contact_count_update', data);
        
        const countElements = document.querySelectorAll('[data-contact-count]');
        countElements.forEach(element => {
            element.textContent = data.count.toLocaleString();
        });
        
        // Update dashboard metrics
        const totalContactsElement = document.querySelector('[data-total-contacts]');
        if (totalContactsElement) {
            totalContactsElement.textContent = data.count.toLocaleString();
        }
        
        // Show notification for significant changes
        if (data.count > data.previous_count) {
            const newContacts = data.count - data.previous_count;
            this.showNotification(
                `${newContacts} new contact${newContacts > 1 ? 's' : ''} added`,
                'info'
            );
        }
    }

    handleNotification(data) {
        this.showNotification(data.message, data.type);
    }

    getStatusColor(status) {
        const colors = {
            'pending': 'secondary',
            'processing': 'warning',
            'completed': 'success',
            'failed': 'danger',
            'cancelled': 'dark'
        };
        return colors[status] || 'secondary';
    }

    showNotification(message, type = 'info') {
        // Use the toast notification component if available
        if (window.Alpine && window.Alpine.store) {
            window.Alpine.store('toast').show(message, type);
        } else {
            // Fallback to browser notification
            if (Notification.permission === 'granted') {
                new Notification('Contact Manager', {
                    body: message,
                    icon: '/static/images/icon.png'
                });
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(permission => {
                    if (permission === 'granted') {
                        new Notification('Contact Manager', {
                            body: message,
                            icon: '/static/images/icon.png'
                        });
                    }
                });
            }
        }
    }

    // Event system
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('Error in SSE event callback:', error);
                }
            });
        }
    }

    // Utility methods
    isConnected() {
        return this.isConnected;
    }

    getConnectionState() {
        if (!this.eventSource) return 'disconnected';
        
        switch (this.eventSource.readyState) {
            case EventSource.CONNECTING: return 'connecting';
            case EventSource.OPEN: return 'connected';
            case EventSource.CLOSED: return 'disconnected';
            default: return 'unknown';
        }
    }
}

// Global SSE manager instance
window.SSEManager = new SSEManager();

// Auto-connect when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only connect if user is authenticated
    if (document.body.dataset.userAuthenticated === 'true') {
        window.SSEManager.connect();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    window.SSEManager.disconnect();
});
