const menuItem = document.querySelectorAll('menu li');

menuItem.forEach(item => {
  console.log(item)
  item.addEventListener('click', function () {
    const subMenu = this.querySelector('ul');
    console.log(subMenu)
    if (subMenu) {
      subMenu.classList.toggle('open');
    }
  });
});