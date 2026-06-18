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

// Menu
document.querySelectorAll('nav > menu.desktop').forEach((menu) => {
  menu.querySelectorAll('li').forEach((item) => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('menu');
    if (submenu) {
      link.addEventListener('click', () => {
        item.classList.toggle('open');

        // Close all other menus (except parents)
        menu.querySelectorAll('li.open').forEach((menuItem) => {
          if (!(menuItem === item || menuItem.contains(item))) {
            menuItem.classList.remove('open');
          }
        });
      });
    }
  });
});

document.addEventListener('click', (event) => {
  document.querySelectorAll('nav > menu.desktop li.open').forEach((item) => {
    if (!item.contains(event.target)) {
      item.classList.remove('open');
    }
  });
});

// Language switcher
const languageSwitcher = document.getElementById('id_language_switcher');
if (languageSwitcher) {
  const toggle = document.getElementById('id_language_switcher_toggle');
  const menu = document.getElementById('id_form_language_menu');

  toggle.addEventListener('click', () => {
    menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', menu.classList.contains('open'));
  });

  document.addEventListener('click', (event) => {
    if (!languageSwitcher.contains(event.target)) {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', false);
    }
  });
}
