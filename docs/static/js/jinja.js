'use strict';

window.initializeJinjaExample = (root) => {
  window.initializeDocsComponent(root);

  const host = root.host;
  const content = root.querySelector('.jinja-example-content');
  let frame;

  function resize() {
    // Remove previously reserved space so closing a menu can shrink the preview
    host.style.width = '';
    host.style.minHeight = '';
    content.style.width = '';
    content.style.transform = '';

    const style = window.getComputedStyle(host);
    const zoom = parseFloat(window.getComputedStyle(content).zoom);
    const bottomInset = parseFloat(style.paddingBottom) + parseFloat(style.borderBottomWidth);

    // Adjust width
    const contentBounds = content.getBoundingClientRect();

    // Keep menu positioning stable while the surrounding preview grows
    content.style.width = `${contentBounds.width / zoom}px`;

    let left = contentBounds.left;
    let right = contentBounds.right;

    root.querySelectorAll('nav menu').forEach((menu) => {
      if (menu.getClientRects().length) {
        const menuBounds = menu.getBoundingClientRect();
        left = Math.min(left, menuBounds.left);
        right = Math.max(right, menuBounds.right);
      }
    });

    const leftOverflow = contentBounds.left - left;
    const rightOverflow = right - contentBounds.right;
    const width = contentBounds.width
      + leftOverflow + rightOverflow
      + parseFloat(style.paddingLeft) + parseFloat(style.paddingRight)
      + parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth);

    host.style.width = `${Math.ceil(width)}px`;
    content.style.transform = `translateX(${leftOverflow / zoom}px)`;

    // Adjust height
    const bounds = host.getBoundingClientRect();
    let bottom = bounds.bottom;

    root.querySelectorAll('nav menu').forEach((menu) => {
      if (menu.getClientRects().length) {
        bottom = Math.max(bottom, menu.getBoundingClientRect().bottom + bottomInset);
      }
    });

    host.style.minHeight = `${Math.ceil(bottom - bounds.top)}px`;
  }

  function scheduleResize() {
    window.cancelAnimationFrame(frame);
    frame = window.requestAnimationFrame(resize);
  }

  window.document.addEventListener('click', scheduleResize);
  window.addEventListener('resize', scheduleResize);
  scheduleResize();
};
