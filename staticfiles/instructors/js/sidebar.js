    document.addEventListener('DOMContentLoaded', function () {
        const toggles = document.querySelectorAll('.dropdown-toggle-custom');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', function () {
                this.parentElement.classList.toggle('dropdown-open');
            });
        });
    });