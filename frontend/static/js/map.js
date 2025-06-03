document.addEventListener('DOMContentLoaded', () => {
  const map = document.getElementById('map-area');
  const pcs = map.querySelectorAll('[draggable]');

  pcs.forEach(pc => {
    pc.addEventListener('dragstart', (e) => {
      const rect = pc.getBoundingClientRect();
      e.dataTransfer.setData('offsetX', e.clientX - rect.left);
      e.dataTransfer.setData('offsetY', e.clientY - rect.top);
      e.dataTransfer.setData('id', pc.dataset.id);
    });
  });

  map.addEventListener('dragover', e => e.preventDefault());

  map.addEventListener('drop', async e => {
    e.preventDefault();
    const offsetX = +e.dataTransfer.getData('offsetX');
    const offsetY = +e.dataTransfer.getData('offsetY');
    const id = e.dataTransfer.getData('id');

    const x = e.offsetX - offsetX;
    const y = e.offsetY - offsetY;

    const el = document.querySelector(`[data-id='${id}']`);
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;

    try {
      await fetch("/map/update-position", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, x, y })
      });
    } catch (error) {
      console.error("Ошибка при сохранении позиции:", error);
    }
  });
});
