import {_} from './gettext.mjs';

// Password fields
document.querySelectorAll('.password-input').forEach((container) => {
  const input = container.querySelector('input');
  const button = container.querySelector('button');
  const iconActive = button.querySelector('.active');
  const iconInactive = button.querySelector('.inactive');

  button.addEventListener('click', () => {
    if (input.type === 'password') {
      input.type = 'text';
      iconActive.style.display = 'block';
      iconInactive.style.display = 'none';
      button.setAttribute('aria-label', _('Hide password'));
      button.setAttribute('title', _('Hide password'));
    } else {
      input.type = 'password';
      iconActive.style.display = 'none';
      iconInactive.style.display = 'block';
      button.setAttribute('aria-label', _('Show password'));
      button.setAttribute('title', _('Show password'));
    }
  });
});

document.querySelectorAll('menu.desktop li').forEach(item => {
  const link = item.querySelector('a');
  const submenu = item.querySelector('ul');

  if (submenu) {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      submenu.classList.toggle('open');

      if (submenu.classList.contains('open')) {
        submenu.querySelectorAll('ul.open').forEach(childSubmenu => {
          childSubmenu.classList.remove('open');
        });
      }
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

    if (expanded) {
      mobileMenu.querySelectorAll('ul.open').forEach(childSubmenu => {
        childSubmenu.classList.remove('open');
      });
    }
  });

  mobileMenu.querySelectorAll('li').forEach(item => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('ul');

    if (submenu) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        submenu.classList.toggle('open');

        if (submenu.classList.contains('open')) {
          submenu.querySelectorAll('ul.open').forEach(childSubmenu => {
            childSubmenu.classList.remove('open');
          });
        }
      });
    }
  });
}

