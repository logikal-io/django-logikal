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
