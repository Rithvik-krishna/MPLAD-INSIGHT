// MPLAD Insight AI - Global Interactive Application Script
document.addEventListener('DOMContentLoaded', () => {
    // 1. Toast Notification System
    function showToast(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'fixed bottom-5 right-5 z-[9999] flex flex-col gap-2 pointer-events-none';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        const bgColors = {
            success: 'bg-emerald-600 text-white',
            error: 'bg-red-600 text-white',
            warning: 'bg-amber-600 text-white',
            info: 'bg-slate-800 text-white'
        };
        const iconNames = {
            success: 'check_circle',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };
        toast.className = `flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-sm font-medium transition-all transform translate-y-2 opacity-0 pointer-events-auto ${bgColors[type] || bgColors.info}`;
        toast.innerHTML = `<span class="material-symbols-outlined text-lg">${iconNames[type] || 'info'}</span><span>${message}</span>`;
        container.appendChild(toast);
        
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-2', 'opacity-0');
        });

        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
    window.showToast = showToast;

    // 2. Interactive action buttons
    document.querySelectorAll('button, a').forEach(btn => {
        const text = (btn.textContent || '').trim().toLowerCase();
        const href = btn.getAttribute('href');
        
        if (!href || href === '#' || href === 'javascript:void(0)') {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if (text.includes('export') || text.includes('download')) {
                    showToast('Generating export report...', 'info');
                    setTimeout(() => showToast('Report downloaded successfully!', 'success'), 1200);
                } else if (text.includes('approve')) {
                    showToast('Case marked as Approved and Compliant.', 'success');
                } else if (text.includes('escalate')) {
                    showToast('Case escalated to District Oversight Committee.', 'warning');
                } else if (text.includes('audit')) {
                    showToast('Physical audit request submitted.', 'info');
                } else if (text.includes('filter') || text.includes('apply')) {
                    showToast('Filters updated.', 'success');
                } else if (text.includes('action req') || text.includes('review case')) {
                    window.location.href = 'Flagged_Cases.html';
                } else if (text.includes('view details') || text.includes('case-')) {
                    window.location.href = 'Case_Details.html';
                } else {
                    showToast('Action: ' + (btn.textContent || 'Click').trim().substring(0, 30), 'info');
                }
            });
        }
    });

    // 3. Make table rows in Flagged Cases clickable
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', (e) => {
            if (e.target.closest('button') || e.target.closest('input') || e.target.closest('a')) return;
            const current = window.location.pathname;
            if (current.includes('Flagged_Cases') || current.includes('Overview_Dashboard') || current.includes('index') || current.endsWith('/')) {
                window.location.href = 'Case_Details.html';
            }
        });
    });

    // 4. Search bar functionality
    document.querySelectorAll('input[type="search"], input[placeholder*="Search"], input[placeholder*="search"]').forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && input.value.trim()) {
                const q = encodeURIComponent(input.value.trim());
                if (!window.location.pathname.includes('Data_Explorer')) {
                    window.location.href = `Data_Explorer.html?q=${q}`;
                } else {
                    showToast(`Filtered for: "${input.value.trim()}"`, 'info');
                }
            }
        });
    });
});
