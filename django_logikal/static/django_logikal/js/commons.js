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

const toggle = document.querySelector('.mobile-menu-toggle');
const dropdown = document.querySelector('.mobile-menu-dropdown');

if (toggle && dropdown) {
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', !expanded);
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
    if (!toggle.contains(e.target) && !dropdown.contains(e.target)) {
      toggle.setAttribute('aria-expanded', 'false');
      dropdown.classList.remove('open');
    }
  });
}