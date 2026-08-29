// MPLAD Insight AI - Forensic Audit & GovTech Oversight Client
document.addEventListener('DOMContentLoaded', () => {
    // 1. Toast Notification Utility
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
            success: 'bg-emerald-800 text-emerald-50 border border-emerald-600',
            error: 'bg-red-800 text-red-50 border border-red-600',
            warning: 'bg-amber-800 text-amber-50 border border-amber-600',
            info: 'bg-slate-900 text-slate-100 border border-slate-700'
        };
        const iconNames = {
            success: 'check_circle',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };
        toast.className = `flex items-center gap-3 px-4 py-3 rounded-lg shadow-xl text-xs font-semibold tracking-wide transition-all transform translate-y-2 opacity-0 pointer-events-auto ${bgColors[type] || bgColors.info}`;
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

    // 2. Universal Global Actions (Export, Audit, Escalations)
    document.querySelectorAll('button, a').forEach(btn => {
        const text = (btn.textContent || '').trim().toLowerCase();
        const href = btn.getAttribute('href');
        
        if (!href || href === '#' || href === 'javascript:void(0)') {
            btn.addEventListener('click', (e) => {
                if (btn.classList.contains('no-toast-intercept') || btn.closest('[data-custom-handler]')) return;
                e.preventDefault();
                
                if (text.includes('export') || text.includes('download')) {
                    showToast('Generating official GovTech audit export...', 'info');
                    setTimeout(() => {
                        exportTableToCSV('mplad-audit-export.csv');
                        showToast('Audit report exported successfully!', 'success');
                    }, 900);
                } else if (text.includes('approve')) {
                    showToast('Work compliance approved. Status logged to central ledger.', 'success');
                } else if (text.includes('escalate')) {
                    showToast('Dossier escalated to District Magistrate & Central Vigilance.', 'warning');
                } else if (text.includes('audit') || text.includes('request audit')) {
                    showToast('Physical verification audit order generated (#ORD-2026-X).', 'info');
                } else if (text.includes('filter') || text.includes('apply')) {
                    showToast('Audit filter matrix updated.', 'info');
                } else if (text.includes('retry') || text.includes('reload')) {
                    showToast('Re-connecting to MoSPI central data pipeline...', 'info');
                    setTimeout(() => location.reload(), 600);
                }
            });
        }
    });

    // 3. Quick Global Search Navigation (Enter key & Cmd/Ctrl+K)
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="Search"], input[placeholder*="search"]');
    searchInputs.forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && input.value.trim()) {
                const q = encodeURIComponent(input.value.trim());
                if (!window.location.pathname.includes('Data_Explorer')) {
                    window.location.href = `Data_Explorer.html?q=${q}`;
                } else {
                    if (window.filterTableRows) window.filterTableRows(input.value.trim());
                    showToast(`Filtered database for query: "${input.value.trim()}"`, 'info');
                }
            }
        });
    });

    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            const firstSearch = document.querySelector('header input');
            if (firstSearch) firstSearch.focus();
        }
    });

    // 4. Utility: Export Table to CSV
    function exportTableToCSV(filename = 'mplad_data.csv') {
        const table = document.querySelector('table');
        if (!table) return;
        let csv = [];
        const rows = table.querySelectorAll('tr');
        for (let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll('td, th');
            for (let j = 0; j < cols.length; j++) {
                let cellText = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, ' ').replace(/"/g, '""').trim();
                row.push('"' + cellText + '"');
            }
            csv.push(row.join(','));
        }
        const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
    window.exportTableToCSV = exportTableToCSV;

    // 5. Automatic Query String filter handling on Data Explorer
    if (window.location.pathname.includes('Data_Explorer')) {
        const urlParams = new URLSearchParams(window.location.search);
        const q = urlParams.get('q');
        if (q) {
            const tableSearch = document.getElementById('table-search') || document.querySelector('input[placeholder*="Search"]');
            if (tableSearch) {
                tableSearch.value = q;
                setTimeout(() => {
                    if (window.filterTableRows) window.filterTableRows(q);
                }, 100);
            }
        }
    }
});
