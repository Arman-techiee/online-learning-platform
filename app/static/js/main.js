// JavaScript file content

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation
    (function () {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms).forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Password strength indicator
    $('#password').on('input', function() {
        const password = $(this).val();
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]+/)) strength++;
        if (password.match(/[A-Z]+/)) strength++;
        if (password.match(/[0-9]+/)) strength++;
        if (password.match(/[$@#&!]+/)) strength++;
        
        let strengthText = '';
        let strengthColor = '';
        
        switch(strength) {
            case 0:
            case 1:
                strengthText = 'Weak';
                strengthColor = 'danger';
                break;
            case 2:
            case 3:
                strengthText = 'Medium';
                strengthColor = 'warning';
                break;
            case 4:
            case 5:
                strengthText = 'Strong';
                strengthColor = 'success';
                break;
        }
        
        $('#password-strength').html(`<small class="text-${strengthColor}">Password Strength: ${strengthText}</small>`);
    });

    // Auto-dismiss alerts
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    $('.delete-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Search functionality
    $('#searchInput').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $('#courseList .course-card').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Smooth scrolling
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if(target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });

    // Course enrollment confirmation
    $('.enroll-btn').on('click', function(e) {
        if (!confirm('Do you want to enroll in this course?')) {
            e.preventDefault();
        }
    });

    // Image preview for file uploads
    $('input[type="file"]').on('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = $(this).siblings('.image-preview');
                if (preview.length === 0) {
                    $(this).after(`<img src="${e.target.result}" class="image-preview img-thumbnail mt-2" style="max-width: 200px;">`);
                } else {
                    preview.attr('src', e.target.result);
                }
            }.bind(this);
            reader.readAsDataURL(file);
        }
    });

    // Dynamic course filtering
    $('#categoryFilter, #difficultyFilter').on('change', function() {
        const category = $('#categoryFilter').val();
        const difficulty = $('#difficultyFilter').val();
        
        $('.course-card').each(function() {
            let show = true;
            
            if (category !== 'all' && $(this).data('category') !== category) {
                show = false;
            }
            
            if (difficulty !== 'all' && $(this).data('difficulty') !== difficulty) {
                show = false;
            }
            
            $(this).toggle(show);
        });
    });

    // Progress bar animation
    $('.progress-bar').each(function() {
        const width = $(this).attr('aria-valuenow');
        $(this).animate({ width: width + '%' }, 1000);
    });

    // Add fade-in animation to elements
    $(window).on('scroll', function() {
        $('.fade-in-scroll').each(function() {
            const elementTop = $(this).offset().top;
            const scrollTop = $(window).scrollTop();
            const windowHeight = $(window).height();
            
            if (scrollTop + windowHeight > elementTop + 100) {
                $(this).addClass('fade-in');
            }
        });
    });
});

// Form submission loading state
function setLoadingState(button) {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    button.disabled = true;
}
