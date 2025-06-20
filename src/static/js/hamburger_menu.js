document.addEventListener('DOMContentLoaded', function () {
    // Hamburger toggle
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav');

    if (hamburger && mobileNav) {
      hamburger.addEventListener('click', function () {
        hamburger.classList.toggle('active');

        if (hamburger.classList.contains('active')) {
          mobileNav.classList.add('active');
        } else {
          mobileNav.classList.remove('active');
        }
      });

      // Menu close when a link is clicked
      const navLinks = mobileNav.querySelectorAll('a[href]');
      navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
          mobileNav.classList.remove('active');
          hamburger.classList.remove('active');
        });
      });
    }
  });