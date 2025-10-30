// Custom Dropdown System (replaces Bootstrap dropdowns)

class CustomDropdown {
    constructor(element) {
        this.element = typeof element === 'string' ? document.querySelector(element) : element;
        this.menu = null;
        this.isShown = false;
        this.init();
    }

    init() {
        if (!this.element) return;

        // Find dropdown menu
        const menu = this.element.querySelector('.dropdown-menu');
        if (!menu) {
            // Try to find menu by ID
            const menuId = this.element.getAttribute('data-target');
            if (menuId) {
                this.menu = document.querySelector(menuId);
            }
        } else {
            this.menu = menu;
        }

        if (!this.menu) return;

        // Toggle on click
        const toggle = this.element.querySelector('.dropdown-toggle') || this.element;
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });
    }

    show() {
        if (this.isShown || !this.menu) return;

        // Hide other dropdowns
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            if (menu !== this.menu) {
                menu.classList.remove('show');
            }
        });

        this.menu.classList.add('show');
        this.isShown = true;

        // Close on outside click
        const closeHandler = (e) => {
            if (!this.element.contains(e.target) && !this.menu.contains(e.target)) {
                this.hide();
                document.removeEventListener('click', closeHandler);
            }
        };
        setTimeout(() => document.addEventListener('click', closeHandler), 0);
    }

    hide() {
        if (!this.isShown || !this.menu) return;

        this.menu.classList.remove('show');
        this.isShown = false;
    }

    toggle() {
        if (this.isShown) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Auto-initialize dropdowns
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        new CustomDropdown(dropdown);
    });
});

// Export
window.CustomDropdown = CustomDropdown;

