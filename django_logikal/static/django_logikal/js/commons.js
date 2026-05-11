const menuItem = document.querySelectorAll('menu li');

menuItem.forEach(item => {
  item.addEventListener('click', function () {
    const subMenu = this.querySelector('ul');
    if (subMenu) {
      const isOpen = subMenu.classList.toggle('open');
      if (isOpen) {
        item.querySelector('svg').style.transform = 'rotate(180deg)';
      }
      else {
        item.querySelector('svg').style.transform = 'rotate(0deg)';
      }
    }
  });
});

document.querySelector('.menu-icon').addEventListener('click', () => {
  document.querySelector('.mobile-menu-dropdown').classList.toggle('open');
});
