// Icon toggles
document.querySelectorAll('button.icon.toggle').forEach((toggle) => {
  const inactiveIcon = toggle.querySelector('.inactive');
  const inactiveTitle = toggle.getAttribute('title');
  const inactiveLabel = toggle.getAttribute('aria-label');
  const activeIcon = toggle.querySelector('.active');
  const activeTitle = toggle.getAttribute('data-active-title');
  const activeLabel = toggle.getAttribute('data-active-aria-label');

  toggle.addEventListener('click', () => {
    if (activeIcon.getAttribute('aria-hidden') === 'true') {
      // Activate
      inactiveIcon.style.display = 'none';
      inactiveIcon.setAttribute('aria-hidden', true);
      activeIcon.style.display = 'block';
      activeIcon.setAttribute('aria-hidden', false);
      toggle.setAttribute('title', activeTitle);
      toggle.setAttribute('aria-label', activeLabel);
    } else {
      // Deactivate
      activeIcon.style.display = 'none';
      activeIcon.setAttribute('aria-hidden', true);
      inactiveIcon.style.display = 'block';
      inactiveIcon.setAttribute('aria-hidden', false);
      toggle.setAttribute('title', inactiveTitle);
      toggle.setAttribute('aria-label', inactiveLabel);
    }
  });
});

// Password fields
document.querySelectorAll('.password-input').forEach((container) => {
  const input = container.querySelector('input');
  const button = container.querySelector('button.icon.toggle');

  button.addEventListener('click', () => {
    input.type = input.type === 'password' ? 'text' : 'password';
  });
});

// Menu
document.querySelectorAll(
  'nav menu.desktop, nav menu.mobile, nav .language-switcher',
).forEach((menu) => {
  menu.querySelectorAll('li').forEach((item) => {
    const button = item.querySelector('button');
    const submenu = item.querySelector('menu');
    if (submenu) {
      button.addEventListener('click', () => {
        item.classList.toggle('open');
        button.setAttribute('aria-expanded', item.classList.contains('open'));

        // Close all other menus (except on mobile, and except parents)
        if (!menu.classList.contains('mobile')) {
          menu.querySelectorAll('li.open').forEach((menuItem) => {
            if (!(menuItem === item || menuItem.contains(item))) {
              menuItem.classList.remove('open');
              menuItem.querySelector('button').setAttribute('aria-expanded', false);
            }
          });
        }
      });
    }
  });
});

window.document.addEventListener('click', (event) => {
  document.querySelectorAll('nav menu.desktop li.open, nav .language-switcher li.open').forEach(
    (item) => {
      if (!event.composedPath().includes(item)) {
        item.classList.remove('open');
        item.querySelector('button').setAttribute('aria-expanded', false);
      }
    },
  );
});

document.querySelectorAll('nav .menu-mobile-container button.icon.toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const menu = button.closest('.menu-mobile-container').querySelector('menu.mobile');
    menu.classList.toggle('open');
    button.setAttribute('aria-expanded', menu.classList.contains('open'));
  });
});

// Notifications
document.querySelectorAll('.notification').forEach((notification) => {
  notification.querySelector('button').addEventListener('click', () => {
    notification.remove();
  });
});
