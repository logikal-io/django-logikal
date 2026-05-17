document.querySelectorAll('.desktop-menu li').forEach(item => {
  const link = item.querySelector('a');
  const submenu = item.querySelector('ul');

  if (submenu) {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      submenu.classList.toggle('open');
    });
  }
});

const menu = document.querySelector('.mobile-menu-icon');
const dropdown = document.querySelector('.mobile-menu');

if (menu && dropdown) {
  menu.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = menu.getAttribute('aria-expanded') === 'true';
    menu.setAttribute('aria-expanded', !expanded);
    dropdown.classList.toggle('open');
  });

  dropdown.querySelectorAll('.mobile-menu li').forEach(item => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('ul');

    if (submenu) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        submenu.classList.toggle('open');
      });
    }
  });

  document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !dropdown.contains(e.target)) {
      menu.setAttribute('aria-expanded', 'false');
      dropdown.classList.remove('open');
    }
  });
}