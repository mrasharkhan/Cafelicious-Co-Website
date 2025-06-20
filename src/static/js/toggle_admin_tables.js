// for show all and hide all toggles
const toggleButtons = document.querySelectorAll('.toggle-table-btn');
      
toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const table = document.getElementById(targetId);

        if (table.style.display === 'none') {
            table.style.display = 'block';
            button.textContent = 'Hide All';
        } else {
            table.style.display = 'none';
            button.textContent = 'Show All';
        }
    });
});