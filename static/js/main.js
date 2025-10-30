// Main JavaScript for Contact Manager

$(document).ready(function() {
    // Initialize DataTables
    $('.data-table').DataTable({
        responsive: true,
        order: [[0, 'desc']],
        pageLength: 25,
        language: {
            search: "Search:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        }
    });
    
    // Initialize tooltips (vanilla JS implementation)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        // Simple tooltip implementation without Bootstrap
        tooltipTriggerEl.addEventListener('mouseenter', function(e) {
            var title = this.getAttribute('title') || this.getAttribute('data-title');
            if (title) {
                var tooltip = document.createElement('div');
                tooltip.className = 'tooltip-custom';
                tooltip.textContent = title;
                document.body.appendChild(tooltip);
                var rect = this.getBoundingClientRect();
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
                tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
                this.tooltipElement = tooltip;
                this.setAttribute('title', '');
            }
        });
        tooltipTriggerEl.addEventListener('mouseleave', function(e) {
            if (this.tooltipElement) {
                document.body.removeChild(this.tooltipElement);
                this.tooltipElement = null;
            }
        });
    });
    
    // Mobile sidebar toggle
    $('#sidebarToggle').on('click', function() {
        $('.sidebar').toggleClass('show');
    });
    
    // Close sidebar on mobile when clicking outside
    $(document).on('click', function(e) {
        if ($(window).width() <= 768 && !$(e.target).closest('.sidebar, #sidebarToggle').length) {
            $('.sidebar').removeClass('show');
        }
    });
    
    // Auto-dismiss alerts after 5 seconds
    $('.alert-dismissible').each(function() {
        var $this = $(this);
        if (!$this.hasClass('alert-permanent')) {
            setTimeout(function() {
                $this.fadeOut(300, function() {
                    $(this).remove();
                });
            }, 5000);
        }
    });
    
    // Form validation
    $('form').on('submit', function(e) {
        var $form = $(this);
        var valid = true;
        
        $form.find('[required]').each(function() {
            if (!$(this).val()) {
                valid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!valid) {
            e.preventDefault();
            Swal.fire({
                icon: 'error',
                title: 'Validation Error',
                text: 'Please fill in all required fields'
            });
        }
    });
    
    // Confirm delete
    $('.delete-btn').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#FF6B35',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = url;
            }
        });
    });
});

// Toast notification helper
function showToast(message, type = 'success') {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });
    
    Toast.fire({
        icon: type,
        title: message
    });
}

// AJAX form submission helper
function submitFormAjax($form, successCallback) {
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize(),
        success: function(response) {
            if (response.success) {
                showToast(response.message || 'Operation successful');
                if (successCallback) successCallback(response);
            } else {
                showToast(response.message || 'Operation failed', 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('An error occurred. Please try again.', 'error');
        }
    });
}

