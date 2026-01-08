// Dark Mode Functionality
(function() {
    'use strict';

    const darkModeToggle = document.getElementById('darkModeToggle') || document.getElementById('darkModeToggleGuest');
    const darkModeIcon = document.getElementById('darkModeIcon') || document.getElementById('darkModeIconGuest');
    const body = document.body;
    
    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme on page load
    body.setAttribute('data-theme', currentTheme);
    updateIcon(currentTheme);
    
    // Toggle dark mode
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
            
            // Add transition effect
            body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        });
    }
    
    function updateIcon(theme) {
        if (darkModeIcon) {
            if (theme === 'dark') {
                darkModeIcon.classList.remove('fa-moon');
                darkModeIcon.classList.add('fa-sun');
            } else {
                darkModeIcon.classList.remove('fa-sun');
                darkModeIcon.classList.add('fa-moon');
            }
        }
    }
})();