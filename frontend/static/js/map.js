document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('pc-grid');
  let draggedEl = null;

  grid.addEventListener('dragstart', e => {
    if (e.target.matches('[draggable]')) {
      draggedEl = e.target;
    }
  });

  grid.addEventListener('dragover', e => {
    e.preventDefault();
    const target = e.target.closest('[draggable]');
    if (target && target !== draggedEl) {
      const draggedIndex = [...grid.children].indexOf(draggedEl);
      const targetIndex = [...grid.children].indexOf(target);
      if (draggedIndex < targetIndex) {
        grid.insertBefore(draggedEl, target.nextSibling);
      } else {
        grid.insertBefore(draggedEl, target);
      }
    }
  });

  grid.addEventListener('drop', async () => {
    const order = [...grid.children].map(el => el.dataset.id);
    try {
      await fetch("/map/update-order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order })
      });
    } catch (error) {
      console.error("Ошибка при сохранении порядка:", error);
    }
  });
});
