// for hamburger and account details toggle action
const hamburger = document.getElementById('hamburger');
const leftPanel = document.getElementById('leftPanel');
const closeBtn = document.getElementById('closeBtn');

hamburger.addEventListener('click', () => {
    leftPanel.classList.add('open');
    hamburger.style.display = 'none';
});

closeBtn.addEventListener('click', () => {
    leftPanel.classList.remove('open');
    hamburger.style.display = 'inline-block';
});

function toggleAccountDetails() {
    const info = document.getElementById('account-info');
    info.style.display = info.style.display === 'block' ? 'none' : 'block';
}