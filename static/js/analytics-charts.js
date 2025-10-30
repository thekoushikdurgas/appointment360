function analyticsDashboard() {
    return {
        isLoading: false,
        selectedDays: 30,
        stats: {
            total_contacts: 0,
            active_contacts: 0,
            total_imports: 0,
            total_exports: 0,
            recent_contacts: 0,
            recent_exports: 0,
            import_success_rate: 0
        },
        charts: {
            industry: null,
            country: null,
            growth: null,
            status: null,
            companies: null
        },

        init() {
            this.loadStats();
            this.loadCharts();
        },

        async loadStats() {
            try {
                const response = await fetch(`/analytics/api/stats/?days=${this.selectedDays}`);
                const data = await response.json();
                
                if (data.error) {
                    console.error('Error loading stats:', data.error);
                    this.showNotification('Failed to load analytics stats', 'error');
                    return;
                }
                
                this.stats = data;
            } catch (error) {
                console.error('Network error loading stats:', error);
                this.showNotification('Network error loading stats', 'error');
            }
        },

        async loadCharts() {
            this.isLoading = true;
            
            try {
                // Load all charts in parallel
                await Promise.all([
                    this.loadChart('industry'),
                    this.loadChart('country'),
                    this.loadChart('growth'),
                    this.loadChart('status'),
                    this.loadChart('companies')
                ]);
            } catch (error) {
                console.error('Error loading charts:', error);
                this.showNotification('Failed to load some charts', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        async loadChart(chartType) {
            try {
                const response = await fetch(`/analytics/api/chart-data/${chartType}/?days=${this.selectedDays}`);
                const data = await response.json();
                
                if (data.error) {
                    console.error(`Error loading ${chartType} chart:`, data.error);
                    this.showChartError(chartType, data.error);
                    return;
                }
                
                this.renderChart(chartType, data);
            } catch (error) {
                console.error(`Network error loading ${chartType} chart:`, error);
                this.showChartError(chartType, 'Network error');
            }
        },

        renderChart(chartType, data) {
            const containerId = `${chartType}-chart`;
            const container = document.getElementById(containerId);
            
            if (!container) {
                console.error(`Chart container not found: ${containerId}`);
                return;
            }

            // Clear any existing content
            container.innerHTML = '';

            try {
                switch (chartType) {
                    case 'industry':
                        this.renderIndustryChart(container, data);
                        break;
                    case 'country':
                        this.renderCountryChart(container, data);
                        break;
                    case 'growth':
                        this.renderGrowthChart(container, data);
                        break;
                    case 'status':
                        this.renderStatusChart(container, data);
                        break;
                    case 'companies':
                        this.renderCompaniesChart(container, data);
                        break;
                    default:
                        console.error(`Unknown chart type: ${chartType}`);
                }
            } catch (error) {
                console.error(`Error rendering ${chartType} chart:`, error);
                this.showChartError(chartType, 'Rendering error');
            }
        },

        renderIndustryChart(container, data) {
            const plotData = [{
                labels: data.labels,
                values: data.values,
                type: 'pie',
                hole: 0.4,
                textinfo: 'label+percent',
                textposition: 'outside',
                marker: {
                    colors: data.colors,
                    line: {
                        color: '#fff',
                        width: 2
                    }
                },
                hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            }];

            const layout = {
                title: {
                    text: 'Contact Distribution by Industry',
                    font: { size: 16 }
                },
                showlegend: true,
                legend: {
                    orientation: 'v',
                    x: 1.05,
                    y: 0.5
                },
                margin: { t: 50, b: 50, l: 50, r: 150 },
                font: { family: 'Arial, sans-serif' }
            };

            Plotly.newPlot(container, plotData, layout, { responsive: true });
        },

        renderCountryChart(container, data) {
            const plotData = [{
                labels: data.labels,
                values: data.values,
                type: 'pie',
                hole: 0.4,
                textinfo: 'label+percent',
                textposition: 'outside',
                marker: {
                    colors: data.colors,
                    line: {
                        color: '#fff',
                        width: 2
                    }
                },
                hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            }];

            const layout = {
                title: {
                    text: 'Contact Distribution by Country',
                    font: { size: 16 }
                },
                showlegend: true,
                legend: {
                    orientation: 'v',
                    x: 1.05,
                    y: 0.5
                },
                margin: { t: 50, b: 50, l: 50, r: 150 },
                font: { family: 'Arial, sans-serif' }
            };

            Plotly.newPlot(container, plotData, layout, { responsive: true });
        },

        renderGrowthChart(container, data) {
            const plotData = [{
                x: data.dates,
                y: data.counts,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Contact Count',
                line: {
                    color: '#FF6B35',
                    width: 3
                },
                marker: {
                    color: '#FF6B35',
                    size: 8
                },
                hovertemplate: '<b>%{x}</b><br>Contacts: %{y}<extra></extra>'
            }];

            const layout = {
                title: {
                    text: 'Contact Growth Over Time',
                    font: { size: 16 }
                },
                xaxis: {
                    title: 'Date',
                    type: 'date'
                },
                yaxis: {
                    title: 'Number of Contacts'
                },
                margin: { t: 50, b: 50, l: 50, r: 50 },
                font: { family: 'Arial, sans-serif' },
                hovermode: 'closest'
            };

            Plotly.newPlot(container, plotData, layout, { responsive: true });
        },

        renderStatusChart(container, data) {
            const plotData = [{
                labels: data.labels,
                values: data.values,
                type: 'pie',
                hole: 0.4,
                textinfo: 'label+percent',
                textposition: 'outside',
                marker: {
                    colors: data.colors,
                    line: {
                        color: '#fff',
                        width: 2
                    }
                },
                hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            }];

            const layout = {
                title: {
                    text: 'Contact Status Distribution',
                    font: { size: 16 }
                },
                showlegend: true,
                legend: {
                    orientation: 'v',
                    x: 1.05,
                    y: 0.5
                },
                margin: { t: 50, b: 50, l: 50, r: 150 },
                font: { family: 'Arial, sans-serif' }
            };

            Plotly.newPlot(container, plotData, layout, { responsive: true });
        },

        renderCompaniesChart(container, data) {
            const plotData = [{
                x: data.companies,
                y: data.counts,
                type: 'bar',
                name: 'Contact Count',
                marker: {
                    color: '#9C27B0',
                    line: {
                        color: '#fff',
                        width: 1
                    }
                },
                hovertemplate: '<b>%{x}</b><br>Contacts: %{y}<extra></extra>'
            }];

            const layout = {
                title: {
                    text: 'Top Companies by Contact Count',
                    font: { size: 16 }
                },
                xaxis: {
                    title: 'Company',
                    tickangle: -45
                },
                yaxis: {
                    title: 'Number of Contacts'
                },
                margin: { t: 50, b: 100, l: 50, r: 50 },
                font: { family: 'Arial, sans-serif' }
            };

            Plotly.newPlot(container, plotData, layout, { responsive: true });
        },

        showChartError(chartType, error) {
            const containerId = `${chartType}-chart`;
            const container = document.getElementById(containerId);
            
            if (container) {
                container.innerHTML = `
                    <div class="chart-loading">
                        <div class="text-center">
                            <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                            <p class="text-muted">Failed to load ${chartType} chart</p>
                            <small class="text-muted">${error}</small>
                        </div>
                    </div>
                `;
            }
        },

        async updateDateRange() {
            await this.loadStats();
            await this.loadCharts();
        },

        async refreshCharts() {
            await this.loadStats();
            await this.loadCharts();
            this.showNotification('Charts refreshed successfully', 'success');
        },

        exportCharts() {
            // Export all charts as images
            const chartTypes = ['industry', 'country', 'growth', 'status', 'companies'];
            
            chartTypes.forEach((chartType, index) => {
                setTimeout(() => {
                    const containerId = `${chartType}-chart`;
                    const container = document.getElementById(containerId);
                    
                    if (container && container.data) {
                        Plotly.downloadImage(container, {
                            format: 'png',
                            width: 800,
                            height: 600,
                            filename: `${chartType}-chart-${new Date().toISOString().split('T')[0]}`
                        });
                    }
                }, index * 500); // Stagger downloads
            });
            
            this.showNotification('Charts export started', 'info');
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
        }
    };
}
