document.querySelectorAll('textarea').forEach((field) => field.addEventListener('input', () => field.setAttribute('aria-invalid', 'false')));

const quickForm = document.querySelector('#quick-scan-form');
if (quickForm) {
  const modes = quickForm.querySelectorAll('.scan-mode');
  const panels = quickForm.querySelectorAll('.quick-panel');
  const fields = { text: quickForm.querySelector('#quick-text'), url: quickForm.querySelector('#quick-url') };
  modes.forEach((mode) => mode.addEventListener('click', () => {
    const selected = mode.dataset.mode;
    quickForm.action = quickForm.dataset[`${selected}Action`];
    modes.forEach((button) => { const active = button === mode; button.classList.toggle('active', active); button.setAttribute('aria-selected', String(active)); });
    panels.forEach((panel) => { panel.hidden = panel.dataset.panel !== selected; });
    Object.entries(fields).forEach(([name, field]) => { field.disabled = name !== selected; });
    fields[selected].focus();
  }));
}
