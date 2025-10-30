/**
 * Progress Tracker Alpine.js Component
 * Manages overall project progress and task completion
 */

function progressTracker() {
    return {
        categories: [],
        tasks: [],
        expandedCategories: [],
        isLoading: false,
        
        init() {
            this.loadData();
        },
        
        get overallProgress() {
            if (this.tasks.length === 0) return 0;
            const completed = this.tasks.filter(task => task.is_completed).length;
            return (completed / this.tasks.length) * 100;
        },
        
        get totalTasks() {
            return this.tasks.length;
        },
        
        get completedTasks() {
            return this.tasks.filter(task => task.is_completed).length;
        },
        
        get remainingTasks() {
            return this.totalTasks - this.completedTasks;
        },
        
        async loadData() {
            this.isLoading = true;
            
            try {
                // Load categories
                const categoriesResponse = await fetch('/api/core/categories/');
                if (categoriesResponse.ok) {
                    const categoriesData = await categoriesResponse.json();
                    this.categories = categoriesData.categories || [];
                }
                
                // Load tasks
                const tasksResponse = await fetch('/api/core/tasks/');
                if (tasksResponse.ok) {
                    const tasksData = await tasksResponse.json();
                    this.tasks = tasksData.tasks || [];
                }
            } catch (error) {
                console.error('Error loading progress data:', error);
                this.showNotification('Failed to load progress data', 'error');
            } finally {
                this.isLoading = false;
            }
        },
        
        getTasksForCategory(categoryName) {
            return this.tasks.filter(task => task.category === categoryName);
        },
        
        toggleCategory(categoryName) {
            const index = this.expandedCategories.indexOf(categoryName);
            if (index > -1) {
                this.expandedCategories.splice(index, 1);
            } else {
                this.expandedCategories.push(categoryName);
            }
        },
        
        async toggleTask(taskId) {
            try {
                const task = this.tasks.find(t => t.id === taskId);
                if (!task) return;
                
                const newStatus = !task.is_completed;
                
                const response = await fetch(`/api/core/tasks/${taskId}/toggle/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({
                        is_completed: newStatus
                    })
                });
                
                if (response.ok) {
                    task.is_completed = newStatus;
                    if (newStatus) {
                        task.completed_at = new Date().toISOString();
                    } else {
                        task.completed_at = null;
                    }
                    
                    // Update category completion percentages
                    this.updateCategoryProgress();
                    
                    this.showNotification(
                        `Task "${task.task_name}" ${newStatus ? 'completed' : 'reopened'}`,
                        newStatus ? 'success' : 'info'
                    );
                } else {
                    const error = await response.json();
                    this.showNotification(error.message || 'Failed to update task', 'error');
                }
            } catch (error) {
                console.error('Error toggling task:', error);
                this.showNotification('Failed to update task', 'error');
            }
        },
        
        updateCategoryProgress() {
            this.categories.forEach(category => {
                const categoryTasks = this.getTasksForCategory(category.name);
                const completedCount = categoryTasks.filter(task => task.is_completed).length;
                category.completed_tasks_count = completedCount;
                category.total_tasks_count = categoryTasks.length;
                category.completion_percentage = categoryTasks.length > 0 
                    ? Math.round((completedCount / categoryTasks.length) * 100 * 10) / 10 
                    : 0;
            });
        },
        
        getPriorityClass(priority) {
            const classes = {
                'HIGH': 'badge-priority-HIGH',
                'MEDIUM': 'badge-priority-MEDIUM',
                'LOW': 'badge-priority-LOW'
            };
            return classes[priority] || 'badge-secondary';
        },
        
        async refreshData() {
            await this.loadData();
            this.showNotification('Progress data refreshed', 'success');
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
            
            // Auto-dismiss after 3 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 3000);
        },
        
        getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                   document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        },
        
        // Export progress data
        exportProgress() {
            const progressData = {
                overall_progress: this.overallProgress,
                total_tasks: this.totalTasks,
                completed_tasks: this.completedTasks,
                remaining_tasks: this.remainingTasks,
                categories: this.categories.map(cat => ({
                    name: cat.name,
                    completion_percentage: cat.completion_percentage,
                    completed_tasks: cat.completed_tasks_count,
                    total_tasks: cat.total_tasks_count
                })),
                tasks: this.tasks.map(task => ({
                    name: task.task_name,
                    category: task.category,
                    priority: task.priority,
                    is_completed: task.is_completed,
                    completed_at: task.completed_at
                })),
                exported_at: new Date().toISOString()
            };
            
            const blob = new Blob([JSON.stringify(progressData, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `progress_report_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showNotification('Progress report exported successfully', 'success');
        }
    };
}

// Global utility functions
window.ProgressTracker = {
    // Initialize progress tracker for any element
    init(element) {
        if (typeof Alpine !== 'undefined') {
            Alpine.data('progressTracker', progressTracker);
        }
    },
    
    // Show notification globally
    showNotification(message, type = 'info') {
        const tracker = new progressTracker();
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
