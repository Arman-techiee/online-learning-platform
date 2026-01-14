// Dark Mode Functionality - Complete and Fixed
(function() {
    'use strict';

    // Get both toggle buttons (for logged in and guest users)
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeToggleGuest = document.getElementById('darkModeToggleGuest');
    const darkModeIcon = document.getElementById('darkModeIcon');
    const darkModeIconGuest = document.getElementById('darkModeIconGuest');
    
    // Get the body element
    const body = document.body;
    
    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme on page load
    applyTheme(currentTheme);
    
    // Function to apply theme
    function applyTheme(theme) {
        body.setAttribute('data-theme', theme);
        updateIcon(theme);
        
        // Also update the html element for better coverage
        document.documentElement.setAttribute('data-theme', theme);
    }
    
    // Function to toggle theme
    function toggleTheme() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Add transition effect
        body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        // Optional: Show a brief notification
        showThemeNotification(newTheme);
    }
    
    // Update icon based on theme
    function updateIcon(theme) {
        const icons = [darkModeIcon, darkModeIconGuest].filter(icon => icon);
        
        icons.forEach(icon => {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
    }
    
    // Add click event listeners to both toggle buttons
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleTheme);
    }
    
    if (darkModeToggleGuest) {
        darkModeToggleGuest.addEventListener('click', toggleTheme);
    }
    
    // Optional: Show theme change notification
    function showThemeNotification(theme) {
        // Remove any existing notification
        const existingNotification = document.querySelector('.theme-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.innerHTML = `
            <i class="fas fa-${theme === 'dark' ? 'moon' : 'sun'}"></i>
            ${theme === 'dark' ? 'Dark' : 'Light'} mode enabled
        `;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${theme === 'dark' ? '#1e293b' : '#ffffff'};
            color: ${theme === 'dark' ? '#f1f5f9' : '#1F2937'};
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 9999;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            font-weight: 500;
            animation: slideInUp 0.3s ease;
            border: 1px solid ${theme === 'dark' ? '#334155' : '#e5e7eb'};
        `;
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInUp {
                from {
                    transform: translateY(100px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            @keyframes slideOutDown {
                from {
                    transform: translateY(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(100px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Add to body
        document.body.appendChild(notification);
        
        // Remove after 2 seconds with animation
        setTimeout(() => {
            notification.style.animation = 'slideOutDown 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 2000);
    }
    
    // Listen for system theme changes (optional)
    if (window.matchMedia) {
        const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        darkModeMediaQuery.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                applyTheme(newTheme);
            }
        });
    }
    
    // Add keyboard shortcut (Ctrl/Cmd + Shift + D) to toggle dark mode
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            toggleTheme();
        }
    });
    
    // Expose toggle function globally for debugging
    window.toggleDarkMode = toggleTheme;
    
    console.log('Dark mode initialized. Current theme:', currentTheme);
    console.log('Keyboard shortcut: Ctrl/Cmd + Shift + D to toggle');
})();