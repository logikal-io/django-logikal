document.querySelectorAll('.desktop-menu li').forEach(item => {
  const link = item.querySelector('a');
  const submenu = item.querySelector('ul');

  if (submenu) {
    link.addEventListener('click', (e) => {
      e.preventDefault();

      const isOpening = !submenu.classList.contains('open');
      submenu.classList.toggle('open');

      if (!isOpening) {
        submenu.querySelectorAll('ul.open').forEach(nestedMenu => {
          nestedMenu.classList.remove('open');
        });
      }
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

    const isOpening = !dropdown.classList.contains('open');
    dropdown.classList.toggle('open');

    if (isOpening) {
      document.body.classList.add('no-scroll');
    } else {
      document.body.classList.remove('no-scroll');
      dropdown.querySelectorAll('ul.open').forEach(nestedMenu => {
        nestedMenu.classList.remove('open');
      });
    }
  });

  dropdown.querySelectorAll('li').forEach(item => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('ul');

    if (submenu) {
      link.addEventListener('click', (e) => {
        e.preventDefault();

        const isOpening = !submenu.classList.contains('open');
        submenu.classList.toggle('open');

        if (!isOpening) {
          submenu.querySelectorAll('ul.open').forEach(nestedMenu => {
            nestedMenu.classList.remove('open');
          });
        }
      });
    }
  });

  document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !dropdown.contains(e.target)) {
      menu.setAttribute('aria-expanded', 'false');
      dropdown.classList.remove('open');
      document.body.classList.remove('no-scroll');

      dropdown.querySelectorAll('ul.open').forEach(nestedMenu => {
        nestedMenu.classList.remove('open');
      });
    }
  });
}