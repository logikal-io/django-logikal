document.querySelectorAll('menu.desktop li').forEach(item => {
  const link = item.querySelector('a');
  const submenu = item.querySelector('ul');

  if (submenu) {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      submenu.classList.toggle('open');
    });
  }
});

const menuIcon = document.querySelector('.mobile-menu-icon');
const mobileMenu = document.querySelector('menu.mobile');

if (menuIcon && mobileMenu) {
  menuIcon.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = menuIcon.getAttribute('aria-expanded') === 'true';
    menuIcon.setAttribute('aria-expanded', !expanded);
    mobileMenu.classList.toggle('open');
  });

  mobileMenu.querySelectorAll('li').forEach(item => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('ul');

    if (submenu) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        submenu.classList.toggle('open');
      });
    }
  });
}
