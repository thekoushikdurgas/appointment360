// Custom Modal System (replaces Bootstrap modals)

class CustomModal {
    constructor(element) {
        this.element = typeof element === 'string' ? document.querySelector(element) : element;
        this.backdrop = null;
        this.isShown = false;
        this.init();
    }

    init() {
        if (!this.element) return;

        // Find close buttons
        const closeButtons = this.element.querySelectorAll('[data-dismiss="modal"], .btn-close');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.hide());
        });

        // Close on backdrop click
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element && e.target.classList.contains('modal')) {
                this.hide();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isShown) {
                this.hide();
            }
        });
    }

    show() {
        if (this.isShown) return;

        // Create backdrop
        this.backdrop = document.createElement('div');
        this.backdrop.className = 'modal-backdrop fade';
        document.body.appendChild(this.backdrop);

        // Show modal
        this.element.classList.add('show');
        this.element.style.display = 'block';
        
        // Trigger fade in
        setTimeout(() => {
            this.backdrop.classList.add('show');
            this.element.classList.add('fade-show');
        }, 10);

        // Prevent body scroll
        document.body.style.overflow = 'hidden';

        this.isShown = true;

        // Dispatch custom event
        const event = new CustomEvent('modal:shown', { detail: { modal: this } });
        this.element.dispatchEvent(event);
    }

    hide() {
        if (!this.isShown) return;

        // Hide backdrop
        if (this.backdrop) {
            this.backdrop.classList.remove('show');
            setTimeout(() => {
                if (this.backdrop && this.backdrop.parentNode) {
                    this.backdrop.parentNode.removeChild(this.backdrop);
                }
                this.backdrop = null;
            }, 300);
        }

        // Hide modal
        this.element.classList.remove('fade-show', 'show');
        setTimeout(() => {
            this.element.style.display = 'none';
        }, 300);

        // Restore body scroll
        document.body.style.overflow = '';

        this.isShown = false;

        // Dispatch custom event
        const event = new CustomEvent('modal:hidden', { detail: { modal: this } });
        this.element.dispatchEvent(event);
    }

    toggle() {
        if (this.isShown) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Bootstrap Modal API compatibility
window.CustomModal = CustomModal;

// Helper functions for compatibility
window.showModal = function(selector) {
    const modal = new CustomModal(selector);
    modal.show();
    return modal;
};

window.hideModal = function(selector) {
    const modal = new CustomModal(selector);
    modal.hide();
};

// Auto-initialize modals
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals triggered by buttons
    document.querySelectorAll('[data-toggle="modal"]').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('data-target') || this.getAttribute('href');
            if (target) {
                const modal = new CustomModal(target);
                modal.show();
            }
        });
    });

    // Initialize existing modals
    document.querySelectorAll('.modal').forEach(modalElement => {
        new CustomModal(modalElement);
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CustomModal;
}

