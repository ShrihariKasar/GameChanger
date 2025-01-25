document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;
    const darkMode = localStorage.getItem('darkMode');

    // Function to enable dark mode
    function enableDarkMode() {
        body.classList.add('bg-dark', 'text-light', 'transition-mode');
        localStorage.setItem('darkMode', 'enabled');
        toggleButton.innerHTML = '<i class="fa-solid fa-sun"></i>';
        toggleButton.setAttribute('aria-label', 'Switch to light mode');
    }

    // Function to disable dark mode
    function disableDarkMode() {
        body.classList.remove('bg-dark', 'text-light', 'transition-mode');
        localStorage.setItem('darkMode', 'disabled');
        toggleButton.innerHTML = '<i class="fa-solid fa-moon"></i>';
        toggleButton.setAttribute('aria-label', 'Switch to dark mode');
    }

    // Check saved preference and apply theme
    if (darkMode === 'enabled') {
        enableDarkMode();
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }

    // Toggle event listener
    toggleButton.addEventListener('click', () => {
        if (body.classList.contains('bg-dark')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    });

    // Tooltip initialization
    toggleButton.setAttribute('data-bs-toggle', 'tooltip');
    toggleButton.setAttribute('title', 'Toggle Dark Mode');
    new bootstrap.Tooltip(toggleButton);
});
