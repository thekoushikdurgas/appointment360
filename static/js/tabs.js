// Custom Tab System (replaces Bootstrap tabs)

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    document.querySelectorAll('[data-toggle="tab"]').forEach(tabTrigger => {
        tabTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href') || this.getAttribute('data-target');
            if (!targetId) return;
            
            const targetPane = document.querySelector(targetId);
            if (!targetPane) return;
            
            // Get the tab container
            const tabContainer = this.closest('.nav-tabs');
            if (!tabContainer) return;
            
            // Remove active class from all tabs and panes
            tabContainer.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            const tabContent = targetPane.closest('.tab-content');
            if (tabContent) {
                tabContent.querySelectorAll('.tab-pane').forEach(pane => {
                    pane.classList.remove('active', 'fade');
                });
            }
            
            // Add active class to clicked tab and target pane
            this.classList.add('active');
            targetPane.classList.add('active', 'fade');
            
            // Dispatch custom event
            const event = new CustomEvent('tab:shown', {
                detail: {
                    tab: this,
                    pane: targetPane
                }
            });
            document.dispatchEvent(event);
        });
    });
});

