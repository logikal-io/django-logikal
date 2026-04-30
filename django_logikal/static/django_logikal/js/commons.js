const menuItem = document.querySelectorAll('menu li');

menuItem.forEach(item => {
  console.log(item)
  item.addEventListener('click', function () {
    const subMenu = this.querySelector('ul');
    console.log(subMenu)
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
