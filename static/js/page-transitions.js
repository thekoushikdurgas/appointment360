// Page Transitions and Loading States for Contact Manager

(function() {
    'use strict';
    
    const PageTransitions = {
        init: function() {
            this.attachLoadingStates();
            this.handleNavigation();
            this.showPageTransition();
        },
        
        attachLoadingStates: function() {
            // Add loading state to forms
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', function(e) {
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        submitBtn.classList.add('loading');
                    }
                });
            });
            
            // Add loading state to links that navigate away
            document.querySelectorAll('a.btn-primary, a.btn-get-started').forEach(link => {
                link.addEventListener('click', function(e) {
                    // Only add loading if it's not a navigation link that needs to stay
                    if (!this.href.includes('#') && this.target !== '_blank') {
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                        
                        setTimeout(() => {
                            // Reset if navigation is still in progress
                            if (this.innerHTML.includes('Loading')) {
                                this.innerHTML = originalText;
                            }
                        }, 3000);
                    }
                });
            });
        },
        
        handleNavigation: function() {
            // Smooth scroll to top on navigation
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        },
        
        showPageTransition: function() {
            // Fade in effect on page load
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.3s ease';
            
            window.addEventListener('load', () => {
                setTimeout(() => {
                    document.body.style.opacity = '1';
                }, 100);
            });
        },
        
        showLoadingOverlay: function() {
            const overlay = document.createElement('div');
            overlay.className = 'page-loading-overlay';
            overlay.innerHTML = `
                <div class="spinner-border text-primary" aria-hidden="true"></div>
                <span class="sr-only" role="status" aria-live="polite">Loading…</span>
            `;
            document.body.appendChild(overlay);
        },
        
        hideLoadingOverlay: function() {
            const overlay = document.querySelector('.page-loading-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => overlay.remove(), 300);
            }
        },
        
        animateMetrics: function() {
            // Animate numbers counting up
            const metricValues = document.querySelectorAll('.metric-value[data-count]');
            metricValues.forEach(metric => {
                const target = parseInt(metric.getAttribute('data-count'));
                const duration = 2000;
                const increment = target / (duration / 16);
                let current = 0;
                
                const update = () => {
                    current += increment;
                    if (current < target) {
                        metric.textContent = Math.floor(current);
                        requestAnimationFrame(update);
                    } else {
                        metric.textContent = target;
                    }
                };
                
                const observer = new IntersectionObserver(entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            update();
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                observer.observe(metric);
            });
        }
    };
    
    // Export to global scope
    window.PageTransitions = PageTransitions;
    
    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        PageTransitions.init();
    });
    
    // Add loading overlay styles
    const style = document.createElement('style');
    style.textContent = `
        .page-loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity 0.3s ease;
            padding: max(0px, env(safe-area-inset-top))
                     max(0px, env(safe-area-inset-right))
                     max(0px, env(safe-area-inset-bottom))
                     max(0px, env(safe-area-inset-left));
        }
        
        .spinner-border {
            width: clamp(2rem, 4vw, 3rem);
            height: clamp(2rem, 4vw, 3rem);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease;
        }
    `;
    document.head.appendChild(style);
})();

