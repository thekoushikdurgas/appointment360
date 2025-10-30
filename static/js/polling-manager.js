/**
 * Enhanced AJAX Polling Manager
 * Provides intelligent polling with exponential backoff and error handling
 */
class PollingManager {
    constructor() {
        this.pollingIntervals = new Map();
        this.defaultConfig = {
            interval: 5000, // 5 seconds
            maxInterval: 30000, // 30 seconds max
            backoffMultiplier: 1.5,
            maxRetries: 3,
            retryDelay: 1000,
            onError: null,
            onSuccess: null,
            onComplete: null
        };
    }

    startPolling(key, url, config = {}) {
        // Stop existing polling for this key
        this.stopPolling(key);
        
        const finalConfig = { ...this.defaultConfig, ...config };
        let currentInterval = finalConfig.interval;
        let retryCount = 0;
        
        const poll = async () => {
            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': this.getCSRFToken()
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                // Reset retry count on success
                retryCount = 0;
                currentInterval = finalConfig.interval;
                
                // Call success callback
                if (finalConfig.onSuccess) {
                    finalConfig.onSuccess(data);
                }
                
                // Schedule next poll
                this.scheduleNextPoll(key, currentInterval);
                
            } catch (error) {
                console.error(`Polling error for ${key}:`, error);
                
                retryCount++;
                
                // Call error callback
                if (finalConfig.onError) {
                    finalConfig.onError(error, retryCount);
                }
                
                if (retryCount < finalConfig.maxRetries) {
                    // Exponential backoff for retries
                    const retryDelay = finalConfig.retryDelay * Math.pow(finalConfig.backoffMultiplier, retryCount - 1);
                    this.scheduleNextPoll(key, retryDelay);
                } else {
                    // Max retries reached, increase interval
                    currentInterval = Math.min(currentInterval * finalConfig.backoffMultiplier, finalConfig.maxInterval);
                    this.scheduleNextPoll(key, currentInterval);
                }
            }
        };
        
        // Start polling immediately
        poll();
    }

    scheduleNextPoll(key, delay) {
        const timeoutId = setTimeout(() => {
            this.pollingIntervals.delete(key);
            // Polling will be restarted by the poll function
        }, delay);
        
        this.pollingIntervals.set(key, timeoutId);
    }

    stopPolling(key) {
        if (this.pollingIntervals.has(key)) {
            clearTimeout(this.pollingIntervals.get(key));
            this.pollingIntervals.delete(key);
        }
    }

    stopAllPolling() {
        this.pollingIntervals.forEach((timeoutId) => {
            clearTimeout(timeoutId);
        });
        this.pollingIntervals.clear();
    }

    isPolling(key) {
        return this.pollingIntervals.has(key);
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }
}

// Global polling manager instance
window.PollingManager = new PollingManager();

// Auto-cleanup on page unload
window.addEventListener('beforeunload', () => {
    window.PollingManager.stopAllPolling();
});

/**
 * Polling Mixin for Alpine.js components
 * Provides easy polling functionality to Alpine components
 */
function pollingMixin(config = {}) {
    return {
        pollingManager: window.PollingManager,
        pollingConfig: {
            interval: 5000,
            maxInterval: 30000,
            backoffMultiplier: 1.5,
            maxRetries: 3,
            retryDelay: 1000,
            ...config
        },
        pollingKey: null,
        isPolling: false,
        lastPollTime: null,
        pollCount: 0,

        startPolling(key, url, customConfig = {}) {
            this.pollingKey = key;
            this.isPolling = true;
            
            const finalConfig = {
                ...this.pollingConfig,
                ...customConfig,
                onSuccess: (data) => {
                    this.handlePollingSuccess(data);
                    if (customConfig.onSuccess) {
                        customConfig.onSuccess(data);
                    }
                },
                onError: (error, retryCount) => {
                    this.handlePollingError(error, retryCount);
                    if (customConfig.onError) {
                        customConfig.onError(error, retryCount);
                    }
                }
            };
            
            this.pollingManager.startPolling(key, url, finalConfig);
        },

        stopPolling() {
            if (this.pollingKey) {
                this.pollingManager.stopPolling(this.pollingKey);
                this.isPolling = false;
                this.pollingKey = null;
            }
        },

        handlePollingSuccess(data) {
            this.lastPollTime = new Date();
            this.pollCount++;
        },

        handlePollingError(error, retryCount) {
            console.error(`Polling error in ${this.pollingKey}:`, error);
        },

        getTimeSinceLastPoll() {
            if (!this.lastPollTime) return null;
            return new Date() - this.lastPollTime;
        },

        getPollingStatus() {
            return {
                isPolling: this.isPolling,
                key: this.pollingKey,
                lastPollTime: this.lastPollTime,
                pollCount: this.pollCount,
                timeSinceLastPoll: this.getTimeSinceLastPoll()
            };
        }
    };
}

// Make polling mixin available globally
window.pollingMixin = pollingMixin;
