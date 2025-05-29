document.addEventListener('DOMContentLoaded', function() {
    const announcementForm = document.getElementById('announcementForm');
    const courseErrorMsg = document.getElementById('courseErrorMsg');
    
    if (announcementForm) {
        announcementForm.addEventListener('submit', function(event) {
            // Check if any course is selected
            const courseSelected = document.querySelector('input[name="course"]:checked');
            
            if (!courseSelected) {
                // Prevent form submission
                event.preventDefault();
                
                // Show error message
                courseErrorMsg.classList.remove('d-none');
                
                // Expand the accordion to show options
                const coursesAccordion = document.getElementById('collapseCourses');
                if (coursesAccordion) {
                    const bsCollapse = new bootstrap.Collapse(coursesAccordion, {
                        show: true
                    });
                }
                
                // Scroll to error
                courseErrorMsg.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
});