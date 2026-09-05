/**
 * NIDHI Assistant - AI Audit Copilot Client
 * Embedded Context-Aware Audit Intelligence Interface for NIDHI TRACE
 */

(function() {
    'use strict';

    // State
    let isOpen = false;
    let isMinimized = false;
    let isGenerating = false;
    let includeContext = true;
    let assistantMode = 'online'; // 'online' | 'demo'
    let conversationHistory = [];

    // Storage Keys
    const STORAGE_KEY_MSGS = 'nidhi_assistant_messages_v1';
    const STORAGE_KEY_OPEN = 'nidhi_assistant_open_v1';

    // Load persisted session
    try {
        const savedMsgs = sessionStorage.getItem(STORAGE_KEY_MSGS);
        if (savedMsgs) conversationHistory = JSON.parse(savedMsgs);
        isOpen = sessionStorage.getItem(STORAGE_KEY_OPEN) === 'true';
    } catch (e) {
        conversationHistory = [];
    }

    // =========================================================================
    // 1. CONTEXT BUILDER (Route & DOM Introspection)
    // =========================================================================

    function detectCurrentRoute() {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('case_details')) return 'case-details';
        if (path.includes('flagged_cases')) return 'flagged-cases';
        if (path.includes('geographic_map')) return 'geographic-map';
        if (path.includes('analytics')) return 'analytics';
        if (path.includes('data_explorer')) return 'data-explorer';
        return 'overview';
    }

    function extractCurrentPageContext() {
        const route = detectCurrentRoute();
        const urlParams = new URLSearchParams(window.location.search);
        const context = {
            page: route,
            timestamp: new Date().toISOString()
        };

        if (route === 'case-details') {
            const caseId = (urlParams.get('id') || document.getElementById('dossier-case-id')?.innerText?.replace('ID:', '') || '').trim();
            context.caseId = caseId || 'MPLAD-03983';
            context.title = document.getElementById('dossier-title')?.innerText || '';
            context.sanctioned = document.getElementById('dossier-sanctioned')?.innerText || '';
            context.utilized = document.getElementById('dossier-disbursed')?.innerText || '';
            context.gapDays = document.getElementById('dossier-gap-days')?.innerText || '';
            context.agency = document.getElementById('dossier-agency')?.innerText || '';
            context.score = document.getElementById('dossier-score-badge')?.innerText?.trim() || '';
            context.severity = document.getElementById('dossier-severity-badge')?.innerText?.trim() || '';
            context.mp = document.getElementById('dossier-mp')?.innerText || '';
            context.location = document.getElementById('dossier-location')?.innerText || '';
        } else if (route === 'flagged-cases') {
            context.stateFilter = document.getElementById('state-filter')?.value || 'all';
            context.anomalyFilter = document.getElementById('anomaly-filter')?.value || 'all';
            context.activeTab = document.querySelector('.sev-pill-active')?.innerText || 'All';
            context.totalFlagged = '25,483';
        } else if (route === 'analytics') {
            context.timespan = document.getElementById('timespan-select')?.value || 'all';
            context.totalCorpus = document.getElementById('badge-total-corpus')?.innerText || '';
            context.utilization = document.getElementById('badge-utilization')?.innerText || '';
            context.scrutiny = document.getElementById('badge-scrutiny')?.innerText || '';
        } else if (route === 'geographic-map') {
            context.selectedState = document.getElementById('state-select')?.value || 'all';
            const cardId = document.getElementById('card-id')?.innerText;
            if (cardId && !document.getElementById('project-card')?.classList.contains('hidden')) {
                const match = cardId.match(/#([A-Z0-9\-]+)/);
                if (match) context.selectedProject = match[1];
            }
        } else if (route === 'data-explorer') {
            context.searchQuery = document.getElementById('table-search')?.value || '';
            context.sectorFilter = document.getElementById('filter-sector')?.value || 'all';
            context.stateFilter = document.getElementById('filter-state')?.value || 'all';
            context.statusFilter = document.getElementById('filter-status')?.value || 'all';
        } else {
            // Overview
            context.totalWorks = '198,116';
            context.totalCorpus = '₹8,501.1 Cr';
            context.flaggedWorks = '25,483';
            context.criticalWorks = '4,112';
            context.scrutinyCorpus = '₹2,001.2 Cr';
        }

        return context;
    }

    function getContextLabel() {
        const ctx = extractCurrentPageContext();
        if (ctx.caseId) return `Viewing Case ${ctx.caseId}`;
        if (ctx.page === 'overview') return `Overview Dashboard`;
        if (ctx.page === 'flagged-cases') return `Flagged Triage Queue`;
        if (ctx.page === 'geographic-map') return `Geographic Risk Map`;
        if (ctx.page === 'analytics') return `Analytics (${ctx.timespan || '2019–26'})`;
        if (ctx.page === 'data-explorer') return `Central Ledger Explorer`;
        return `NIDHI TRACE`;
    }

    // =========================================================================
    // 2. DOM INJECTION & UI RENDERING
    // =========================================================================

    function createAssistantDOM() {
        if (document.getElementById('nidhi-assistant-root')) return;

        const root = document.createElement('div');
        root.id = 'nidhi-assistant-root';
        root.className = 'font-sans select-none';

        root.innerHTML = `
            <!-- Floating AI Assistant Button (48px) -->
            <div id="nidhi-assistant-btn-wrap" class="fixed bottom-5 right-5 z-[9990] flex items-center group">
                <!-- Tooltip badge -->
                <div class="mr-2 px-2.5 py-1 bg-slate-900 text-white rounded-md text-[11px] font-bold tracking-wide shadow-md border border-slate-700 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
                    Ask NIDHI
                </div>

                <button id="nidhi-assistant-toggle" type="button" aria-label="Open NIDHI Assistant" class="w-12 h-12 rounded-full bg-slate-900 hover:bg-blue-600 text-white shadow-xl border border-blue-500/40 flex items-center justify-center transition-all transform hover:scale-105 active:scale-95 cursor-pointer relative">
                    <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                    <!-- Online indicator dot -->
                    <span id="nidhi-status-dot" class="absolute top-0.5 right-0.5 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-slate-900"></span>
                </button>
            </div>

            <!-- Floating Chat Panel Drawer (380-420px, max 82vh) -->
            <div id="nidhi-assistant-drawer" class="fixed bottom-20 right-5 z-[9995] w-[410px] max-w-[calc(100vw-24px)] h-[600px] max-h-[82vh] bg-white rounded-xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden transition-all duration-200 transform origin-bottom-right opacity-0 scale-95 pointer-events-none">
                
                <!-- Drawer Header -->
                <div class="px-4 py-3 bg-brand-900 border-b border-slate-800 text-white flex items-center justify-between shrink-0">
                    <div class="flex items-center gap-2.5 min-w-0">
                        <div class="w-7 h-7 rounded-lg bg-blue-600/20 border border-blue-400/40 flex items-center justify-center text-blue-400 shrink-0">
                            <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <div class="flex items-center gap-1.5 leading-tight">
                                <span class="font-extrabold text-xs tracking-wider text-white">NIDHI Assistant</span>
                                <span id="nidhi-drawer-status" class="px-1.5 py-0.2 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 text-[8.5px] font-mono font-bold">● Online</span>
                            </div>
                            <span class="text-[9.5px] text-blue-300/90 font-medium">AI Audit Copilot</span>
                        </div>
                    </div>

                    <!-- Header Actions -->
                    <div class="flex items-center gap-1 text-slate-300">
                        <button id="nidhi-btn-new-chat" type="button" title="New Conversation" class="p-1 hover:text-white hover:bg-slate-800 rounded transition-colors cursor-pointer">
                            <span class="material-symbols-outlined text-base">restart_alt</span>
                        </button>
                        <button id="nidhi-btn-minimize" type="button" title="Minimize Drawer" class="p-1 hover:text-white hover:bg-slate-800 rounded transition-colors cursor-pointer">
                            <span class="material-symbols-outlined text-base">expand_more</span>
                        </button>
                        <button id="nidhi-btn-close" type="button" title="Close Assistant" class="p-1 hover:text-white hover:bg-slate-800 rounded transition-colors cursor-pointer">
                            <span class="material-symbols-outlined text-base">close</span>
                        </button>
                    </div>
                </div>

                <!-- Messages Container -->
                <div id="nidhi-messages-body" class="flex-1 min-h-0 p-3.5 overflow-y-auto space-y-3 bg-slate-50/50 text-xs">
                    <!-- Dynamic Messages & Welcome State -->
                </div>

                <!-- Context Attachment Indicator Bar -->
                <div id="nidhi-context-strip" class="px-3 py-1.5 bg-slate-100/90 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-600 shrink-0">
                    <div class="flex items-center gap-1.5 truncate pr-2">
                        <span class="material-symbols-outlined text-xs text-blue-600 shrink-0">attachment</span>
                        <span class="font-medium text-slate-500">Context:</span>
                        <span id="nidhi-context-label" class="font-mono font-bold text-slate-800 truncate">Detecting route...</span>
                    </div>
                    <button id="nidhi-toggle-context" type="button" class="text-blue-600 hover:text-blue-800 font-bold shrink-0 hover:underline">
                        Enabled
                    </button>
                </div>

                <!-- Chat Input Strip -->
                <form id="nidhi-input-form" class="p-2.5 bg-white border-t border-borderline flex items-center gap-2 shrink-0">
                    <div class="relative flex-1">
                        <textarea id="nidhi-user-input" rows="1" class="w-full pl-3 pr-8 py-2 text-xs rounded-lg border border-slate-300 bg-slate-50 text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-blue-600 focus:ring-1 focus:ring-blue-600 outline-none resize-none font-sans leading-tight max-h-24" placeholder="Ask about MPLAD data, risks, or this case..."></textarea>
                    </div>
                    <button id="nidhi-send-btn" type="submit" class="w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center shrink-0 shadow-2xs transition-all disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer" title="Send Question">
                        <span class="material-symbols-outlined text-base">send</span>
                    </button>
                </form>

                <!-- Persistent Compliance Disclaimer -->
                <div class="px-3 py-1 bg-slate-100 border-t border-slate-200/70 text-center text-[9px] text-slate-500 font-medium shrink-0">
                    AI-generated analysis. Verify against official records before taking audit action.
                </div>
            </div>
        `;

        document.body.appendChild(root);
        bindEvents();
        checkBackendStatus();
        renderConversation();
    }

    // =========================================================================
    // 3. UI INTERACTION & EVENT BINDINGS
    // =========================================================================

    function bindEvents() {
        const toggleBtn = document.getElementById('nidhi-assistant-toggle');
        const closeBtn = document.getElementById('nidhi-btn-close');
        const minBtn = document.getElementById('nidhi-btn-minimize');
        const newChatBtn = document.getElementById('nidhi-btn-new-chat');
        const form = document.getElementById('nidhi-input-form');
        const input = document.getElementById('nidhi-user-input');
        const toggleCtxBtn = document.getElementById('nidhi-toggle-context');

        toggleBtn?.addEventListener('click', toggleDrawer);
        closeBtn?.addEventListener('click', closeDrawer);
        minBtn?.addEventListener('click', closeDrawer);
        newChatBtn?.addEventListener('click', startNewChat);

        toggleCtxBtn?.addEventListener('click', () => {
            includeContext = !includeContext;
            toggleCtxBtn.innerText = includeContext ? 'Enabled' : 'Disabled';
            toggleCtxBtn.className = includeContext ? 'text-blue-600 hover:text-blue-800 font-bold shrink-0 hover:underline' : 'text-slate-400 font-bold shrink-0 hover:underline';
            updateContextLabel();
        });

        input?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                form.dispatchEvent(new Event('submit'));
            }
        });

        form?.addEventListener('submit', handleFormSubmit);

        // Auto-update context label on page focus or route changes
        window.addEventListener('focus', updateContextLabel);
        updateContextLabel();
    }

    function toggleDrawer() {
        if (isOpen) {
            closeDrawer();
        } else {
            openDrawer();
        }
    }

    function openDrawer() {
        const drawer = document.getElementById('nidhi-assistant-drawer');
        if (!drawer) return;
        isOpen = true;
        sessionStorage.setItem(STORAGE_KEY_OPEN, 'true');

        drawer.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
        drawer.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');

        updateContextLabel();
        setTimeout(() => {
            document.getElementById('nidhi-user-input')?.focus();
        }, 150);
        scrollMessagesToBottom();
    }

    function closeDrawer() {
        const drawer = document.getElementById('nidhi-assistant-drawer');
        if (!drawer) return;
        isOpen = false;
        sessionStorage.setItem(STORAGE_KEY_OPEN, 'false');

        drawer.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
        drawer.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
    }

    function updateContextLabel() {
        const labelEl = document.getElementById('nidhi-context-label');
        if (labelEl) {
            labelEl.innerText = includeContext ? getContextLabel() : 'Context Detached';
        }
    }

    function startNewChat() {
        conversationHistory = [];
        sessionStorage.removeItem(STORAGE_KEY_MSGS);
        renderConversation();
        document.getElementById('nidhi-user-input')?.focus();
    }

    async function checkBackendStatus() {
        try {
            const res = await fetch('/api/assistant/status');
            if (res.ok) {
                const data = await res.json();
                assistantMode = data.mode || 'online';
                const statusBadge = document.getElementById('nidhi-drawer-status');
                const statusDot = document.getElementById('nidhi-status-dot');
                if (data.status === 'demo') {
                    if (statusBadge) {
                        statusBadge.className = 'px-1.5 py-0.2 rounded-full bg-amber-950 text-amber-300 border border-amber-800 text-[8.5px] font-mono font-bold';
                        statusBadge.innerText = '● Demo Mode';
                    }
                    if (statusDot) {
                        statusDot.className = 'absolute top-0.5 right-0.5 w-2.5 h-2.5 bg-amber-500 rounded-full border-2 border-slate-900';
                    }
                }
            }
        } catch (e) {
            console.warn("[NIDHI Assistant] Status check failed:", e);
        }
    }

    // =========================================================================
    // 4. RENDERING CONVERSATION & SUGGESTIONS
    // =========================================================================

    function renderConversation() {
        const body = document.getElementById('nidhi-messages-body');
        if (!body) return;

        if (!conversationHistory || conversationHistory.length === 0) {
            renderWelcomeState(body);
            return;
        }

        let html = '';
        conversationHistory.forEach(msg => {
            if (msg.role === 'user') {
                html += `
                    <div class="flex justify-end">
                        <div class="max-w-[85%] bg-slate-900 text-white rounded-2xl rounded-br-xs px-3.5 py-2 shadow-2xs leading-relaxed text-xs">
                            ${escapeHtml(msg.content)}
                        </div>
                    </div>
                `;
            } else {
                const formattedContent = formatMarkdown(msg.content);
                const sourceBadge = msg.source ? `
                    <div class="mt-1.5 pt-1 border-t border-slate-200/80 text-[9.5px] font-mono font-medium text-slate-500 flex items-center gap-1">
                        <span class="material-symbols-outlined text-xs text-blue-600">verified</span>
                        <span>${escapeHtml(msg.source)}</span>
                    </div>
                ` : '';

                html += `
                    <div class="flex items-start gap-2">
                        <div class="w-6 h-6 rounded-full bg-brand-900 border border-blue-500/40 text-blue-400 flex items-center justify-center shrink-0 mt-0.5 shadow-2xs">
                            <span class="material-symbols-outlined text-xs" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                        </div>
                        <div class="max-w-[88%] bg-white border border-slate-200 rounded-2xl rounded-bl-xs p-3 shadow-2xs text-slate-800 text-xs space-y-1.5 leading-relaxed">
                            <div class="prose-content">${formattedContent}</div>
                            ${sourceBadge}
                        </div>
                    </div>
                `;
            }
        });

        body.innerHTML = html;
        scrollMessagesToBottom();
    }

    function renderWelcomeState(container) {
        const route = detectCurrentRoute();
        const urlParams = new URLSearchParams(window.location.search);
        const hasCaseId = Boolean(urlParams.get('id'));

        let suggestions = [];
        if (route === 'case-details' || hasCaseId) {
            suggestions = [
                "Why was this case flagged?",
                "Explain this risk score",
                "Summarize this project",
                "Which signal contributed most?",
                "Compare this project with the baseline"
            ];
        } else {
            suggestions = [
                "Why are projects being flagged?",
                "Explain the risk score",
                "Show me the highest-risk cases",
                "What does MP Spending Habit Drift mean?",
                "Explain Isolation Forest",
                "How is Scrutiny Exposure calculated?"
            ];
        }

        const pillsHtml = suggestions.map(q => `
            <button type="button" onclick="window.nidhiSendSuggested('${escapeHtml(q)}')" class="text-left px-2.5 py-1.5 bg-white border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 rounded-lg text-[11px] text-slate-700 font-medium transition-all shadow-2xs flex items-center justify-between group cursor-pointer">
                <span>${escapeHtml(q)}</span>
                <span class="material-symbols-outlined text-xs text-slate-400 group-hover:text-blue-600 transition-colors">arrow_forward</span>
            </button>
        `).join('');

        container.innerHTML = `
            <div class="py-4 px-2 space-y-3.5">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-blue-600/10 border border-blue-500/30 flex items-center justify-center text-blue-600 shrink-0">
                        <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                    </div>
                    <div>
                        <h3 class="font-extrabold text-slate-900 text-xs">How can I help with this dashboard?</h3>
                        <p class="text-[10px] text-slate-500 mt-0.5">Ask about MPLAD works, anomalies, risk scores, audit indicators, or visible data.</p>
                    </div>
                </div>

                <div class="space-y-1.5">
                    <span class="text-[9.5px] font-bold text-slate-400 uppercase tracking-wider block">Suggested Questions</span>
                    <div class="grid grid-cols-1 gap-1.5">
                        ${pillsHtml}
                    </div>
                </div>
            </div>
        `;
    }

    window.nidhiSendSuggested = function(question) {
        const input = document.getElementById('nidhi-user-input');
        if (input) input.value = question;
        document.getElementById('nidhi-input-form')?.dispatchEvent(new Event('submit'));
    };

    // =========================================================================
    // 5. MESSAGE DISPATCH & API CALL
    // =========================================================================

    async function handleFormSubmit(e) {
        e.preventDefault();
        if (isGenerating) return;

        const input = document.getElementById('nidhi-user-input');
        const text = (input?.value || '').trim();
        if (!text) return;

        // Add user message
        conversationHistory.push({ role: 'user', content: text });
        input.value = '';
        renderConversation();
        setGeneratingState(true);

        // Gather context
        const pageContext = includeContext ? extractCurrentPageContext() : { page: 'detached' };

        try {
            const res = await fetch('/api/assistant/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    pageContext: pageContext,
                    conversation: conversationHistory.slice(-6)
                })
            });

            const data = await res.json();
            const reply = data.message || "NIDHI Assistant couldn't complete that request. Please try again.";
            const source = data.source || (data.mode === 'demo' ? 'Local Knowledge Engine (Demo Mode)' : 'Based on NIDHI TRACE data');

            conversationHistory.push({
                role: 'assistant',
                content: reply,
                source: source
            });

            // Save in session
            sessionStorage.setItem(STORAGE_KEY_MSGS, JSON.stringify(conversationHistory.slice(-10)));

        } catch (err) {
            console.error("[NIDHI Assistant] Communication error:", err);
            conversationHistory.push({
                role: 'assistant',
                content: "NIDHI Assistant couldn't complete that request. Please verify connection and try again.",
                source: "System Error"
            });
        } finally {
            setGeneratingState(false);
            renderConversation();
        }
    }

    function setGeneratingState(loading) {
        isGenerating = loading;
        const sendBtn = document.getElementById('nidhi-send-btn');
        const body = document.getElementById('nidhi-messages-body');

        if (sendBtn) sendBtn.disabled = loading;

        if (loading && body) {
            const loadingIndicator = document.createElement('div');
            loadingIndicator.id = 'nidhi-loading-bubble';
            loadingIndicator.className = 'flex items-center gap-2';
            loadingIndicator.innerHTML = `
                <div class="w-6 h-6 rounded-full bg-brand-900 border border-blue-500/40 text-blue-400 flex items-center justify-center shrink-0 shadow-2xs">
                    <span class="material-symbols-outlined text-xs animate-spin">refresh</span>
                </div>
                <div class="bg-white border border-slate-200 rounded-2xl rounded-bl-xs px-3.5 py-2 text-[11px] text-slate-500 font-medium flex items-center gap-2 shadow-2xs">
                    <span class="animate-pulse">Analyzing NIDHI TRACE context...</span>
                </div>
            `;
            body.appendChild(loadingIndicator);
            scrollMessagesToBottom();
        } else {
            document.getElementById('nidhi-loading-bubble')?.remove();
        }
    }

    function scrollMessagesToBottom() {
        const body = document.getElementById('nidhi-messages-body');
        if (body) {
            body.scrollTop = body.scrollHeight;
        }
    }

    // =========================================================================
    // 6. UTILITIES (Markdown & Escaping)
    // =========================================================================

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function formatMarkdown(text) {
        if (!text) return '';
        let s = escapeHtml(text);

        // Headers
        s = s.replace(/^### (.*$)/gim, '<h4 class="font-bold text-slate-900 text-xs mt-2 mb-1 border-b border-slate-100 pb-0.5">$1</h4>');
        s = s.replace(/^## (.*$)/gim, '<h3 class="font-bold text-slate-900 text-xs mt-2 mb-1">$1</h3>');

        // Bold & Italic
        s = s.replace(/\*\*(.*?)\*\*/gim, '<strong class="font-bold text-slate-900">$1</strong>');
        s = s.replace(/\*(.*?)\*/gim, '<em class="italic text-slate-700">$1</em>');

        // Monospace inline code / tags
        s = s.replace(/`([^`]+)`/gim, '<code class="px-1 py-0.2 rounded bg-slate-100 border border-slate-200 font-mono text-[10px] text-slate-800 font-semibold">$1</code>');

        // Blockquotes
        s = s.replace(/^> (.*$)/gim, '<blockquote class="p-2 my-1 bg-blue-50/60 border-l-2 border-blue-500 rounded-r text-[10.5px] text-blue-950 font-medium">$1</blockquote>');

        // Bullet points
        s = s.replace(/^\s*[-•]\s+(.*$)/gim, '<div class="flex items-start gap-1.5 my-0.5"><span class="text-blue-600 font-bold">•</span><span>$1</span></div>');

        // Numbered lists
        s = s.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<div class="flex items-start gap-1.5 my-0.5"><span class="font-mono text-slate-500 font-bold">$1.</span><span>$2</span></div>');

        // Line breaks
        s = s.replace(/\n\n/g, '<div class="h-1.5"></div>');

        return s;
    }

    // =========================================================================
    // 7. INITIALIZATION
    // =========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createAssistantDOM);
    } else {
        createAssistantDOM();
    }

    // If opened previously in session, restore state
    if (isOpen) {
        setTimeout(openDrawer, 300);
    }

})();
