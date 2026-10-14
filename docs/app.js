const menuButton = document.querySelector('.menu-button');
const navLinks = document.querySelector('.nav-links');

if (menuButton && navLinks) {
  menuButton.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });

  navLinks.addEventListener('click', (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navLinks.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
    }
  });
}

document.querySelectorAll('.copy-button').forEach((button) => {
  button.addEventListener('click', async () => {
    const code = button.closest('.code-block')?.querySelector('code');
    if (!code) return;

    const previousLabel = button.textContent;
    try {
      await navigator.clipboard.writeText(code.textContent ?? '');
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Select text';
    }

    window.setTimeout(() => {
      button.textContent = previousLabel;
    }, 1600);
  });
});

