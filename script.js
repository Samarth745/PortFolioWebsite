document.addEventListener('DOMContentLoaded', () => {
  const navigationLinks = document.querySelectorAll('nav.links a[href^="#"]');

  navigationLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navigationLinks.forEach((item) => item.removeAttribute('aria-current'));
      link.setAttribute('aria-current', 'page');
    });
  });
});
