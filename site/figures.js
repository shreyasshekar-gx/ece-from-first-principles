import { phone, hub, dish } from './vendor/hairline/index.js';

const factories = { phone, hub, dish };
const figures = new Map();

function mountFigures() {
  // Hash navigation and carousel changes replace nodes. Dispose the old engines
  // so their observers, pointer listeners, and animation work do not survive.
  for (const [element, figure] of figures) {
    if (!element.isConnected) {
      figure.destroy();
      figures.delete(element);
    }
  }
  for (const element of document.querySelectorAll('[data-hairline]')) {
    if (figures.has(element)) continue;
    const factory = factories[element.dataset.hairline];
    if (!factory) continue;
    const figure = factory(element, {
      play: false,
      intensity: 0.65,
      theme: 'auto',
      label: element.dataset.label,
    });
    figures.set(element, figure);
    element.closest('.hairline-plate')?.classList.add('is-mounted');
  }
}

document.addEventListener('ece:figures', mountFigures);
window.addEventListener('pagehide', () => {
  for (const figure of figures.values()) figure.destroy();
  figures.clear();
});
window.addEventListener('pageshow', mountFigures);
mountFigures();
