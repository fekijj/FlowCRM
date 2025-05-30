document.addEventListener('DOMContentLoaded', () => {
  async function loadStats() {
    try {
      const pcs = await fetch('/api/pcs').then(r => r.json());
      document.getElementById('active-pcs').textContent = pcs.filter(pc => pc.is_online).length;

      const stats = await fetch('/api/stats').then(r => r.json());
      document.getElementById('sales-today').textContent = stats.sales_today;
      document.getElementById('total-revenue').textContent = stats.total_revenue + ' ₽';
    } catch (err) {
      console.error("Ошибка при загрузке данных:", err);
    }
  }

  loadStats();
});
