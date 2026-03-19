// MotoGama Elite — JS principal

document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
        flash.style.transition = 'opacity 0.4s, transform 0.4s';
        flash.style.opacity = '0';
        flash.style.transform = 'translateX(120%)';
        setTimeout(() => flash.remove(), 400);
    }, 4000);
});

document.querySelectorAll('.form-delete').forEach(form => {
    form.addEventListener('submit', e => {
        if (!confirm('¿Estás seguro de que deseas eliminar este registro? Esta acción no se puede deshacer.')) {
            e.preventDefault();
        }
    });
});

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(target)?.classList.add('active');
    });
});

document.querySelectorAll('input[name="valor"], input[name="precio"]').forEach(input => {
    input.addEventListener('input', () => {
        const raw = input.value.replace(/[^0-9.]/g, '');
        input.value = raw;
    });
});

const vehiculoSelect = document.getElementById('id_vehiculo');
const valorInput = document.getElementById('valor_venta');
if (vehiculoSelect && valorInput) {
    vehiculoSelect.addEventListener('change', async () => {
        const id = vehiculoSelect.value;
        if (!id) return;
        try {
            const res = await fetch(`/api/vehiculo/${id}`);
            const data = await res.json();
            if (data.precio) {
                valorInput.value = data.precio;
            }
        } catch (e) {
            console.error(e);
        }
    });
}

document.querySelectorAll('.stat-value[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const isFloat = el.dataset.float === 'true';
    const duration = 800;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(timer); }
        el.textContent = isFloat
            ? '$' + Math.round(current).toLocaleString('es-CO')
            : Math.round(current).toLocaleString('es-CO');
    }, 16);
});
