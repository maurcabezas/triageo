// Triageo Dashboard Application Logic

const apiHost = window.location.hostname;
const API_URL = `http://${apiHost}:8004/api/v1`;

// Sample ticket presets
const TICKET_PRESETS = [
    {
        id: "preset-gdpr",
        label: "GDPR Deletion",
        emoji: "🛡️",
        subject: "I need to delete my account and all my data",
        description: "Please delete all personal data under GDPR Article 17. I want everything removed immediately. This is my formal request.",
        customer_tier: "free"
    },
    {
        id: "preset-billing",
        label: "Refund Request",
        emoji: "💳",
        subject: "Charge on my card after cancellation",
        description: "I canceled my pro plan subscription last week, but I was still charged $29 today. Please refund this amount.",
        customer_tier: "pro"
    },
    {
        id: "preset-bug",
        label: "App Crash",
        emoji: "🐛",
        subject: "Application crashes on dashboard load",
        description: "Every time I login and open the dashboard tab, the app freezes and then crashes with a segmentation fault error. I've cleared my cache but it persists.",
        customer_tier: "enterprise"
    },
    {
        id: "preset-login",
        label: "Account Locked",
        emoji: "🔒",
        subject: "Locked out of my account: incorrect password attempts",
        description: "I tried typing my password too many times and now my admin account is locked. I need to regain access as we have an active deployment.",
        customer_tier: "enterprise"
    },
    {
        id: "preset-docs",
        label: "Broken Links",
        emoji: "📄",
        subject: "404 Error in API docs references",
        description: "The link to the authentication guides inside the API documentation returns a 404 Not Found error. Can you point me to the correct page?",
        customer_tier: "free"
    }
];

// DOM Elements
const apiStatusIndicator = document.getElementById("api-status-indicator");
const apiStatusText = document.getElementById("api-status-text");
const presetsContainer = document.getElementById("presets-container");
const triageForm = document.getElementById("triage-form");
const subjectInput = document.getElementById("subject");
const descriptionInput = document.getElementById("description");
const tierSelect = document.getElementById("customer_tier");
const submitBtn = document.getElementById("submit-btn");

const emptyStateEl = document.getElementById("no-results");
const loadingStateEl = document.getElementById("loading");
const resultsContentEl = document.getElementById("results-content");

const resTicketId = document.getElementById("result-ticket-id");
const resCategory = document.getElementById("result-category");
const resPriority = document.getElementById("result-priority");
const priorityDot = document.getElementById("priority-dot");
const resTeam = document.getElementById("result-team");
const resConfidence = document.getElementById("result-confidence");
const resHumanReview = document.getElementById("result-human-review");
const resReasoning = document.getElementById("result-reasoning");
const resKbContext = document.getElementById("result-kb-context");

const traceLine = document.getElementById("trace-line");
const traceStatusBadge = document.getElementById("trace-status-badge");

// Graph Node Elements
const nodes = {
    classify: document.getElementById("node-classify"),
    retrieve: document.getElementById("node-retrieve"),
    route: document.getElementById("node-route"),
    review: document.getElementById("node-review"),
    finalize: document.getElementById("node-finalize")
};

// Check API health periodically
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_URL.replace("/api/v1", "")}/health`);
        if (response.ok) {
            apiStatusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block";
            apiStatusText.textContent = "API Online";
        } else {
            throw new Error("API unhealthy");
        }
    } catch (err) {
        apiStatusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500 inline-block";
        apiStatusText.textContent = "API Offline";
    }
}

// Initialise Presets UI
function initPresets() {
    presetsContainer.innerHTML = "";
    TICKET_PRESETS.forEach(preset => {
        const card = document.createElement("button");
        card.type = "button";
        card.className = "preset-card text-left px-3 py-2 bg-surface hover:bg-surface-container border border-outline-variant rounded-lg text-sm text-on-surface transition-all flex items-center gap-2 w-full";
        card.id = preset.id;
        card.innerHTML = `
            <div class="preset-emoji text-base">${preset.emoji}</div>
            <div class="font-semibold text-xs text-on-surface">${preset.label}</div>
        `;
        
        card.addEventListener("click", () => {
            // Toggle active class
            document.querySelectorAll(".preset-card").forEach(c => {
                c.classList.remove("active", "border-primary", "bg-primary-light");
            });
            card.classList.add("active", "border-primary", "bg-primary-light");
            
            // Populate form
            subjectInput.value = preset.subject;
            descriptionInput.value = preset.description;
            tierSelect.value = preset.customer_tier;
        });
        
        presetsContainer.appendChild(card);
    });
}

// Reset trace UI back to pending state
function resetTraceUI() {
    traceLine.style.width = "0%";
    traceStatusBadge.textContent = "Idle";
    traceStatusBadge.className = "px-3 py-1 bg-surface-container text-on-surface-variant rounded-full text-xs font-bold uppercase tracking-wider shadow-sm";
    
    Object.keys(nodes).forEach(key => {
        const circle = nodes[key].querySelector(".node-circle");
        const name = nodes[key].querySelector(".node-name");
        
        circle.className = "w-8 h-8 rounded-full bg-surface-container-highest text-on-surface-variant flex items-center justify-center border-4 border-surface-container-low shadow-sm mb-1 node-circle transition-all";
        name.className = "text-[10px] font-label font-bold text-on-surface-variant uppercase node-name";
    });
}

// Visualise the active node transition
async function animateGraphTrace() {
    resetTraceUI();
    traceStatusBadge.textContent = "Running";
    traceStatusBadge.className = "px-3 py-1 bg-amber-100 text-amber-800 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm";

    const nodeSequence = ['classify', 'retrieve', 'route', 'review', 'finalize'];
    
    // Simulate trace execution
    for (let i = 0; i < nodeSequence.length; i++) {
        const current = nodeSequence[i];
        const circle = nodes[current].querySelector(".node-circle");
        const name = nodes[current].querySelector(".node-name");
        
        // Make active
        circle.className = "w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center border-4 border-surface-container-low shadow-sm mb-1 node-circle transition-all ring-4 ring-amber-100 animate-pulse";
        name.className = "text-[10px] font-label font-bold text-primary uppercase node-name";
        
        // Wait brief moment for realism
        await new Promise(r => setTimeout(r, 600));
        
        // Make completed
        circle.className = "w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center border-4 border-emerald-100 shadow-sm mb-1 node-circle transition-all";
        name.className = "text-[10px] font-label font-bold text-emerald-700 uppercase node-name";
        
        // Update trace line
        traceLine.style.width = `${(i / (nodeSequence.length - 1)) * 100}%`;
    }
}

// Highlight all nodes as finished (for history loads)
function setTraceCompleted(requiresReview) {
    traceLine.style.width = "100%";
    traceStatusBadge.textContent = requiresReview ? "Needs Review" : "Auto Resolved";
    traceStatusBadge.className = `px-3 py-1 ${requiresReview ? 'bg-red-100 text-red-800' : 'bg-emerald-100 text-emerald-800'} rounded-full text-xs font-bold uppercase tracking-wider shadow-sm`;

    Object.keys(nodes).forEach(key => {
        const circle = nodes[key].querySelector(".node-circle");
        const name = nodes[key].querySelector(".node-name");
        circle.className = "w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center border-4 border-emerald-100 shadow-sm mb-1 node-circle transition-all";
        name.className = "text-[10px] font-label font-bold text-emerald-700 uppercase node-name";
    });
}

// Handle Form Submission
triageForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Get values
    const payload = {
        subject: subjectInput.value.trim(),
        description: descriptionInput.value.trim(),
        customer_tier: tierSelect.value
    };

    // UI state
    emptyStateEl.classList.add("hidden");
    resultsContentEl.classList.add("hidden");
    loadingStateEl.classList.remove("hidden");
    submitBtn.disabled = true;

    try {
        // Start trace animation concurrently
        const animPromise = animateGraphTrace();
        
        const response = await fetch(`${API_URL}/triage`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server returned error status: ${response.status}`);
        }

        const data = await response.json();
        
        // Wait for graph animation to complete so UI flows smoothly
        await animPromise;

        // Render response data
        renderResults(data);
        traceStatusBadge.textContent = data.requires_human_review ? "Needs Review" : "Auto Resolved";
        traceStatusBadge.className = `px-3 py-1 ${data.requires_human_review ? 'bg-red-100 text-red-800' : 'bg-emerald-100 text-emerald-800'} rounded-full text-xs font-bold uppercase tracking-wider shadow-sm`;

        // Refresh triage history list
        loadHistory();
        
    } catch (error) {
        console.error("Triage request failed:", error);
        alert(`Failed to complete triage request: ${error.message}. Is the API service running and accessible?`);
        emptyStateEl.classList.remove("hidden");
        resetTraceUI();
    } finally {
        loadingStateEl.classList.add("hidden");
        submitBtn.disabled = false;
    }
});

// Render results
function renderResults(data) {
    resTicketId.textContent = data.ticket_id;
    
    // Category text
    resCategory.textContent = data.category.replace("_", " ").toUpperCase();
    
    // Priority Badge & Indicator Dot
    resPriority.textContent = data.priority.toUpperCase();
    if (data.priority === "low") {
        resPriority.className = "text-base font-semibold text-slate-500";
        priorityDot.className = "w-3 h-3 rounded-full bg-slate-400";
    } else if (data.priority === "medium") {
        resPriority.className = "text-base font-semibold text-sky-600";
        priorityDot.className = "w-3 h-3 rounded-full bg-sky-500";
    } else if (data.priority === "high") {
        resPriority.className = "text-base font-semibold text-amber-600";
        priorityDot.className = "w-3 h-3 rounded-full bg-amber-500";
    } else {
        resPriority.className = "text-base font-semibold text-red-600 animate-pulse";
        priorityDot.className = "w-3 h-3 rounded-full bg-red-600 animate-pulse";
    }
    
    resTeam.textContent = data.recommended_team.toUpperCase();
    resConfidence.textContent = `${(data.confidence * 100).toFixed(0)}%`;
    
    // Human Review Badge
    const needsReview = data.requires_human_review;
    resHumanReview.textContent = needsReview ? "YES — ESCALATED" : "NO — AUTO RESOLVED";
    resHumanReview.className = `badge font-bold text-xs px-2.5 py-1 rounded-full ${needsReview ? 'bg-red-100 text-red-700 border border-red-200' : 'bg-emerald-100 text-emerald-700 border border-emerald-200'}`;
    
    resReasoning.textContent = data.reasoning;
    
    // KB Context
    resKbContext.innerHTML = "";
    if (data.retrieved_context && data.retrieved_context.length > 0) {
        data.retrieved_context.forEach(snippet => {
            // Snippets are formatted like: "[doc-id] Title: excerpt..."
            const match = snippet.match(/^\[(.*?)\] (.*?): (.*)$/);
            
            const docEl = document.createElement("div");
            docEl.className = "p-3 bg-surface-container-low hover:bg-surface-container border border-outline-variant rounded-lg transition-colors flex items-start gap-4";
            
            if (match) {
                const [_, docId, title, excerpt] = match;
                docEl.innerHTML = `
                    <div class="w-10 h-10 rounded bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center shrink-0">
                        <span class="material-symbols-outlined text-xl">article</span>
                    </div>
                    <div class="flex-1">
                        <h4 class="font-semibold text-sm text-on-surface">${title}</h4>
                        <p class="text-xs text-on-surface-variant mt-1 line-clamp-2">${excerpt}</p>
                    </div>
                    <div class="text-xs font-label px-2 py-1 bg-surface-variant rounded text-on-surface-variant whitespace-nowrap">${docId}</div>
                `;
            } else {
                docEl.innerHTML = `
                    <div class="w-10 h-10 rounded bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center shrink-0">
                        <span class="material-symbols-outlined text-xl">article</span>
                    </div>
                    <div class="flex-1">
                        <p class="text-xs text-on-surface-variant mt-1">${snippet}</p>
                    </div>
                `;
            }
            resKbContext.appendChild(docEl);
        });
    } else {
        resKbContext.innerHTML = `<div class="text-xs text-on-surface-variant italic py-2">No matching knowledge base documentation found.</div>`;
    }

    resultsContentEl.classList.remove("hidden");
}

// --- History Persistence and Panel Logic ---
let historyCache = [];
const historyContainer = document.getElementById("history-container");

async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/triage/history?limit=10`);
        if (!response.ok) throw new Error("Failed to fetch history");
        const data = await response.json();
        historyCache = data;
        renderHistoryList(data);
    } catch (err) {
        console.error("Failed to load history list:", err);
    }
}

function renderHistoryList(items) {
    if (!items || items.length === 0) {
        historyContainer.innerHTML = `<div class="history-empty text-xs text-on-surface-variant italic text-center py-4">No recent triage runs.</div>`;
        return;
    }

    historyContainer.innerHTML = "";
    items.forEach((item, index) => {
        const itemEl = document.createElement("div");
        itemEl.className = "history-item p-3 bg-surface border border-outline-variant rounded-lg flex flex-col gap-2 hover:border-primary transition-colors cursor-pointer";
        itemEl.dataset.index = index;

        let prioClass = "";
        if (item.priority === "low") prioClass = "bg-slate-100 text-slate-800";
        else if (item.priority === "medium") prioClass = "bg-sky-100 text-sky-800";
        else if (item.priority === "high") prioClass = "bg-amber-100 text-amber-800";
        else prioClass = "bg-red-100 text-red-800";

        let timeStr = "Just now";
        if (item.created_at) {
            try {
                const date = new Date(item.created_at + "Z"); // Parse as UTC
                timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            } catch (e) {}
        }

        itemEl.innerHTML = `
            <div class="flex justify-between items-start">
                <span class="text-[10px] font-label font-bold text-on-surface-variant">${item.ticket_id.toUpperCase()}</span>
                <span class="px-2 py-0.5 text-[9px] font-bold rounded uppercase tracking-wider ${prioClass}">${item.priority}</span>
            </div>
            <p class="text-sm font-semibold text-on-surface line-clamp-1">${escapeHtml(item.subject)}</p>
            <div class="flex justify-between items-center mt-1">
                <span class="text-[9px] text-on-surface-variant">Routed: ${item.recommended_team.toUpperCase()}</span>
                <span class="text-[9px] text-on-surface-variant">${timeStr}</span>
            </div>
        `;

        itemEl.addEventListener("click", () => {
            selectHistoryItem(index, itemEl);
        });

        historyContainer.appendChild(itemEl);
    });
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function selectHistoryItem(index, element) {
    document.querySelectorAll(".history-item").forEach(el => el.classList.remove("border-primary", "bg-primary-light"));
    element.classList.add("border-primary", "bg-primary-light");

    const item = historyCache[index];
    
    // Fill inputs
    subjectInput.value = item.subject;
    descriptionInput.value = item.description;
    tierSelect.value = item.customer_tier || "free";

    // Set trace nodes to Completed
    setTraceCompleted(item.requires_human_review);

    // Render output
    renderResults(item);
    
    emptyStateEl.classList.add("hidden");
    loadingStateEl.classList.add("hidden");
    resultsContentEl.classList.remove("hidden");
}

// Initialize
initPresets();
checkApiHealth();
loadHistory();
setInterval(checkApiHealth, 10000); // Check health every 10 seconds
