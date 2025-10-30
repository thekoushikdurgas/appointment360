// Onboarding/Tour Functionality for Contact Manager

(function() {
    'use strict';
    
    const OnboardingTour = {
        currentStep: 0,
        steps: [],
        isActive: false,
        localStorageKey: 'contact_manager_onboarding_completed',
        
        init: function() {
            // Check if user has completed onboarding
            if (this.hasCompletedOnboarding()) {
                return;
            }
            
            this.defineSteps();
            this.startTour();
        },
        
        defineSteps: function() {
            this.steps = [
                {
                    element: '[data-tour="welcome"]',
                    title: 'Welcome to Contact Manager! 👋',
                    content: 'Let\'s take a quick tour of your dashboard. I\'ll show you the key features.',
                    position: 'bottom'
                },
                {
                    element: '[data-tour="metrics"]',
                    title: 'Key Metrics 📊',
                    content: 'Here you can see important statistics about your contacts at a glance.',
                    position: 'top'
                },
                {
                    element: '[data-tour="charts"]',
                    title: 'Data Visualization 📈',
                    content: 'Interactive charts help you understand your contact distribution by industry and country.',
                    position: 'top'
                },
                {
                    element: '[data-tour="quick-actions"]',
                    title: 'Quick Actions 🚀',
                    content: 'Access your most used features quickly from here.',
                    position: 'top'
                },
                {
                    element: '[data-tour="navigation"]',
                    title: 'Navigation Menu',
                    content: 'Navigate to different sections of the application using the sidebar menu.',
                    position: 'right'
                }
            ];
        },
        
        startTour: function() {
            this.isActive = true;
            this.showWelcomeModal();
        },
        
        showWelcomeModal: function() {
            const modal = this.createModal(`
                <div class="text-center">
                    <i class="fas fa-address-book fa-4x text-primary mb-3"></i>
                    <h3>Welcome to Contact Manager! 🎉</h3>
                    <p class="text-muted">Would you like to take a quick tour of the dashboard?</p>
                    <div class="d-flex gap-2 justify-content-center mt-4">
                        <button class="btn btn-primary" onclick="OnboardingTour.proceedWithTour()">
                            <i class="fas fa-play"></i> Start Tour
                        </button>
                        <button class="btn btn-outline-secondary" onclick="OnboardingTour.skipTour()">
                            <i class="fas fa-times"></i> Skip Tour
                        </button>
                    </div>
                </div>
            `);
            this.showModal(modal);
        },
        
        proceedWithTour: function() {
            this.closeModal();
            this.attachTourStyles();
            this.showStep(0);
        },
        
        skipTour: function() {
            this.closeModal();
            this.markCompleted();
        },
        
        showStep: function(stepIndex) {
            if (stepIndex >= this.steps.length) {
                this.completeTour();
                return;
            }
            
            this.currentStep = stepIndex;
            const step = this.steps[stepIndex];
            
            // Find element
            const element = document.querySelector(step.element);
            if (!element) {
                this.showStep(stepIndex + 1);
                return;
            }
            
            // Scroll to element
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Add highlight overlay
            this.addHighlight(element);
            
            // Show tooltip
            setTimeout(() => {
                this.showTooltip(element, step, stepIndex);
            }, 300);
        },
        
        addHighlight: function(element) {
            // Remove existing highlights
            document.querySelectorAll('.tour-highlight').forEach(el => el.remove());
            
            const rect = element.getBoundingClientRect();
            const highlight = document.createElement('div');
            highlight.className = 'tour-highlight';
            highlight.style.cssText = `
                position: fixed;
                top: ${rect.top}px;
                left: ${rect.left}px;
                width: ${rect.width}px;
                height: ${rect.height}px;
                pointer-events: none;
                z-index: 9998;
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
                border: 3px solid #FF6B35;
                border-radius: 12px;
                animation: pulse 2s ease-in-out infinite;
            `;
            document.body.appendChild(highlight);
        },
        
        showTooltip: function(element, step, stepIndex) {
            // Remove existing tooltips
            document.querySelectorAll('.tour-tooltip').forEach(el => el.remove());
            
            const rect = element.getBoundingClientRect();
            const tooltip = document.createElement('div');
            tooltip.className = 'tour-tooltip';
            
            const stepIndicator = `${stepIndex + 1} of ${this.steps.length}`;
            const nextButtonText = stepIndex === this.steps.length - 1 ? 'Finish Tour' : 'Next';
            const nextButtonIcon = stepIndex === this.steps.length - 1 ? 'check' : 'arrow-right';
            
            tooltip.innerHTML = `
                <div class="tour-tooltip-header">
                    <h5>${step.title}</h5>
                    <button onclick="OnboardingTour.closeTooltip()" class="tour-close-btn">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="tour-tooltip-content">
                    <p>${step.content}</p>
                </div>
                <div class="tour-tooltip-footer">
                    <div class="tour-progress">
                        <div class="tour-progress-bar" style="width: ${((stepIndex + 1) / this.steps.length) * 100}%"></div>
                    </div>
                    <div class="tour-buttons">
                        ${stepIndex > 0 ? `
                            <button onclick="OnboardingTour.previousStep()" class="btn btn-outline-secondary btn-sm">
                                <i class="fas fa-arrow-left"></i> Previous
                            </button>
                        ` : ''}
                        <button onclick="OnboardingTour.nextStep()" class="btn btn-primary btn-sm">
                            ${nextButtonText} <i class="fas fa-${nextButtonIcon}"></i>
                        </button>
                    </div>
                </div>
            `;
            
            // Position tooltip
            let top = rect.bottom + 20;
            let left = rect.left + (rect.width / 2) - 200;
            
            if (step.position === 'top') {
                top = rect.top - 250;
            }
            
            if (left < 20) left = 20;
            if (left + 400 > window.innerWidth) left = window.innerWidth - 420;
            
            var isDark = document.documentElement.classList.contains('theme-dark');
            var tooltipBg = isDark ? 'var(--card)' : 'white';
            var tooltipText = isDark ? 'var(--text)' : '#333';
            tooltip.style.cssText = `
                position: fixed;
                top: ${top}px;
                left: ${left}px;
                z-index: 10000;
                background: ${tooltipBg};
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
                padding: 1.5rem;
                width: 400px;
                animation: slideIn 0.3s ease;
                color: ${tooltipText};
            `;
            
            document.body.appendChild(tooltip);
        },
        
        nextStep: function() {
            this.closeTooltip();
            this.showStep(this.currentStep + 1);
        },
        
        previousStep: function() {
            this.closeTooltip();
            this.showStep(this.currentStep - 1);
        },
        
        closeTooltip: function() {
            document.querySelectorAll('.tour-tooltip').forEach(el => el.remove());
            document.querySelectorAll('.tour-highlight').forEach(el => el.remove());
        },
        
        completeTour: function() {
            this.closeTooltip();
            this.detachTourStyles();
            this.markCompleted();
            
            const modal = this.createModal(`
                <div class="text-center">
                    <i class="fas fa-check-circle fa-4x text-success mb-3"></i>
                    <h3>Tour Complete! 🎉</h3>
                    <p class="text-muted">You're all set to start managing your contacts!</p>
                    <button class="btn btn-primary mt-3" onclick="OnboardingTour.closeModal()">
                        <i class="fas fa-check"></i> Let's Go!
                    </button>
                </div>
            `);
            this.showModal(modal);
        },
        
        markCompleted: function() {
            localStorage.setItem(this.localStorageKey, 'true');
        },
        
        hasCompletedOnboarding: function() {
            return localStorage.getItem(this.localStorageKey) === 'true';
        },
        
        resetOnboarding: function() {
            localStorage.removeItem(this.localStorageKey);
        },
        
        attachTourStyles: function() {
            if (document.getElementById('tour-styles')) return;
            
            const style = document.createElement('style');
            style.id = 'tour-styles';
            style.textContent = `
                @keyframes pulse {
                    0%, 100% { opacity: 0.8; }
                    50% { opacity: 1; }
                }
                
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .tour-highlight {
                    transition: all 0.3s ease;
                }
                
                .tour-tooltip {
                    animation: slideIn 0.3s ease;
                }
                
                .tour-tooltip-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1rem;
                    padding-bottom: 0.75rem;
                    border-bottom: 2px solid #e9ecef;
                }
                
                .tour-tooltip-header h5 { margin: 0; }
                
                .tour-close-btn {
                    background: none;
                    border: none;
                    color: #6c757d;
                    cursor: pointer;
                    padding: 0.25rem 0.5rem;
                }
                
                .tour-tooltip-content {
                    margin-bottom: 1rem;
                }
                
                .tour-tooltip-footer {
                    margin-top: 1rem;
                }
                
                .tour-progress {
                    height: 4px;
                    background: #e9ecef;
                    border-radius: 2px;
                    margin-bottom: 1rem;
                    overflow: hidden;
                }
                
                .tour-progress-bar {
                    height: 100%;
                    background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
                    transition: width 0.3s ease;
                }
                
                .tour-buttons {
                    display: flex;
                    justify-content: space-between;
                    gap: 0.5rem;
                }
                
                .tour-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10001;
                    animation: fadeIn 0.3s ease;
                }
                
                .tour-modal-content {
                    background: ${'${isDark ? "var(--card)" : "white"}'};
                    border-radius: 12px;
                    padding: 2rem;
                    max-width: 500px;
                    width: 90%;
                    animation: slideUp 0.3s ease;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                
                @keyframes slideUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            `;
            document.head.appendChild(style);
        },
        
        detachTourStyles: function() {
            const style = document.getElementById('tour-styles');
            if (style) style.remove();
        },
        
        createModal: function(content) {
            const modal = document.createElement('div');
            modal.className = 'tour-modal';
            modal.innerHTML = `
                <div class="tour-modal-content">${content}</div>
            `;
            return modal;
        },
        
        showModal: function(modal) {
            document.body.appendChild(modal);
            // Close on outside click
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    OnboardingTour.closeModal();
                }
            });
        },
        
        closeModal: function() {
            document.querySelectorAll('.tour-modal').forEach(el => el.remove());
        }
    };
    
    // Export to global scope
    window.OnboardingTour = OnboardingTour;
    
    // Auto-start on page load
    document.addEventListener('DOMContentLoaded', function() {
        OnboardingTour.init();
    });
})();

