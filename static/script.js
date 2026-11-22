document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const loading = document.getElementById('loading');
    const leadsContainer = document.getElementById('leadsContainer');
    const leadCount = document.getElementById('leadCount');

    let pollInterval = null;

    // Load initial leads
    fetchLeads();

    searchBtn.addEventListener('click', async () => {
        const niche = document.getElementById('niche').value.trim();
        const location = document.getElementById('location').value.trim();

        if (!niche || !location) {
            alert('Zəhmət olmasa, həm sahə, həm də məkanı daxil edin!');
            return;
        }

        loading.classList.remove('hidden');
        searchBtn.disabled = true;
        searchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analiz edilir...';

        try {
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ niche, location, use_mock: false })
            });
            const data = await res.json();
            if (!res.ok) {
                // 422 from server-side validation (blank, too long, multi-line input)
                throw new Error(JSON.stringify(data.detail || data));
            }

            // Poll for results every 3 seconds
            if (pollInterval) clearInterval(pollInterval);
            pollInterval = setInterval(async () => {
                await fetchLeads();
            }, 3000);

            // Stop polling after 60 seconds
            setTimeout(() => {
                if (pollInterval) clearInterval(pollInterval);
                loading.classList.add('hidden');
                searchBtn.disabled = false;
                searchBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Müştəriləri Tap';
            }, 60000);

        } catch (err) {
            console.error(err);
            alert('Axtarışa başlayarkən xəta baş verdi.');
            loading.classList.add('hidden');
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Müştəriləri Tap';
        }
    });

    refreshBtn.addEventListener('click', () => {
        fetchLeads();
    });

    async function fetchLeads() {
        try {
            const res = await fetch('/api/leads');
            const data = await res.json();
            renderLeads(data.leads);

            // If all leads are processed, stop polling
            if (data.leads.length > 0 && data.leads.every(l => l.status === 'processed')) {
                if (pollInterval) clearInterval(pollInterval);
                loading.classList.add('hidden');
                searchBtn.disabled = false;
                searchBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Müştəriləri Tap';
            }
        } catch (err) {
            console.error('Failed to fetch leads', err);
        }
    }

    function renderLeads(leads) {
        leadCount.textContent = leads.length;
        leadsContainer.innerHTML = '';

        if (leads.length === 0) {
            leadsContainer.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">Hələ heç bir müştəri tapılmayıb. Axtarışa başlayın!</p>';
            return;
        }

        leads.forEach(lead => {
            const isProcessed = lead.status === 'processed';
            const card = document.createElement('div');
            card.className = 'lead-card';

            const systemIcon = getSystemIcon(lead.best_system);

            card.innerHTML = `
                <div class="lead-header">
                    <div>
                        <h3>${escapeHtml(lead.business_name)}</h3>
                        <a href="${escapeHtml(lead.profile_url)}" target="_blank">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Profilə Bax
                        </a>
                    </div>
                    <span class="status ${isProcessed ? 'processed' : 'new'}">
                        ${isProcessed
                            ? '<i class="fa-solid fa-check"></i> AI Hazırdır'
                            : '<i class="fa-solid fa-spinner fa-spin"></i> Analiz edilir...'}
                    </span>
                </div>

                <div class="lead-body">
                    <div class="lead-section">
                        <h4><i class="fa-solid fa-address-book"></i> Əlaqə</h4>
                        <p>${escapeHtml(lead.contact_info || 'Tapılmadı')}</p>
                    </div>

                    ${isProcessed ? `
                        <div class="lead-section system-highlight">
                            <h4>${systemIcon} Ən Gəlirli Sistem</h4>
                            <p class="best-system-tag">${escapeHtml(lead.best_system || 'N/A')}</p>
                        </div>

                        <div class="lead-section">
                            <h4><i class="fa-solid fa-chart-line"></i> Niyə Bu Sistem?</h4>
                            <p class="why-box">${escapeHtml(lead.why_this_system || 'N/A')}</p>
                        </div>

                        <div class="lead-section">
                            <h4><i class="fa-solid fa-dollar-sign"></i> Aylıq Əlavə Gəlir</h4>
                            <p class="revenue-box">${escapeHtml(lead.estimated_revenue || 'N/A')}</p>
                        </div>

                        <div class="lead-section">
                            <h4><i class="fa-brands fa-instagram"></i> AI DM Mesajı</h4>
                            <div class="message-box-wrapper">
                                <p class="message-box">${escapeHtml(lead.ai_message || 'N/A')}</p>
                                <button class="copy-btn" onclick="copyText(this, \`${escapeBt(lead.ai_message)}\`)">
                                    <i class="fa-solid fa-copy"></i> Kopyala
                                </button>
                            </div>
                        </div>
                    ` : `
                        <div class="lead-section">
                            <p style="text-align:center; color:var(--text-muted); font-style:italic;">
                                <i class="fa-solid fa-robot"></i> Süni intellekt bu müştərinin profilini analiz edir...
                            </p>
                        </div>
                    `}
                </div>
            `;
            leadsContainer.appendChild(card);
        });
    }

    function getSystemIcon(system) {
        if (!system) return '<i class="fa-solid fa-robot"></i>';
        const s = system.toLowerCase();
        if (s.includes('booking') || s.includes('appointment')) return '<i class="fa-solid fa-calendar-check"></i>';
        if (s.includes('crm') || s.includes('qualifier')) return '<i class="fa-solid fa-users-gear"></i>';
        if (s.includes('dm') || s.includes('instagram')) return '<i class="fa-brands fa-instagram"></i>';
        if (s.includes('whatsapp')) return '<i class="fa-brands fa-whatsapp"></i>';
        if (s.includes('loyalty') || s.includes('repeat')) return '<i class="fa-solid fa-heart"></i>';
        if (s.includes('review')) return '<i class="fa-solid fa-star"></i>';
        if (s.includes('cart') || s.includes('ecommerce') || s.includes('product')) return '<i class="fa-solid fa-cart-shopping"></i>';
        return '<i class="fa-solid fa-robot"></i>';
    }

    function escapeHtml(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function escapeBt(text) {
        if (!text) return '';
        return String(text).replace(/`/g, "'").replace(/\$/g, '\\$');
    }
});

function copyText(btn, text) {
    navigator.clipboard.writeText(text).then(() => {
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Kopyalandı!';
        setTimeout(() => {
            btn.innerHTML = '<i class="fa-solid fa-copy"></i> Kopyala';
        }, 2000);
    });
}
