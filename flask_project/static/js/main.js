// Library Management System JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // Auto fade-out alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Real-time table search/filter
    const searchInput = document.getElementById('tableSearch');
    const table = document.getElementById('booksTable');
    if (searchInput && table) {
        searchInput.addEventListener('keyup', () => {
            const query = searchInput.value.toLowerCase().trim();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Default dates for Book Issue Form
    const issueDateInput = document.getElementById('issue_date');
    const returnDateInput = document.getElementById('return_date');
    if (issueDateInput && !issueDateInput.value) {
        const today = new Date();
        issueDateInput.value = today.toISOString().split('T')[0];
        
        if (returnDateInput && !returnDateInput.value) {
            const dueDate = new Date();
            dueDate.setDate(today.getDate() + 14); // 14 days default
            returnDateInput.value = dueDate.toISOString().split('T')[0];
        }
    }
});
