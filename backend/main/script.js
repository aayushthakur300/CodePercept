// Run this only after the HTML page finishes loading
document.addEventListener('DOMContentLoaded', () => {

    // --- Buttons and main editor elements ---
    const runBtn = document.getElementById('runBtn');
    const fullFixBtn = document.getElementById('fullFixBtn');
    const codeInput = document.getElementById('codeInput');
    const lineNumArea = document.getElementById("editorLineNumbers");


    
    // ================================
    // LINE NUMBER SYNC SYSTEM
    // ================================
    function updateEditorLineNumbers() {
        const code = codeInput.value;
        const totalLines = code.split("\n").length;

        // Create line numbers 1..N
        const linesArray = new Array(totalLines);
        for (let i = 0; i < totalLines; i++) linesArray[i] = i + 1;

        // Update the line number column
        lineNumArea.innerHTML = linesArray.join("<br>");

        // Sync scroll to match the code editor
        lineNumArea.scrollTop = codeInput.scrollTop;
    }

    // Update line numbers when typing
    codeInput.addEventListener("input", updateEditorLineNumbers);

    // Sync scroll for both areas
    codeInput.addEventListener("scroll", () => {
        lineNumArea.scrollTop = codeInput.scrollTop;
    });

    // ================================
    // CUSTOM TAB INDENTATION
    // ================================
    codeInput.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();  // prevent switching focus

            const start = this.selectionStart;
            const end = this.selectionEnd;

            // Insert 4 spaces
            const spaces = "    ";
            this.value =
                this.value.substring(0, start) +
                spaces +
                this.value.substring(end);

            // Move cursor after the inserted spaces
            this.selectionStart = this.selectionEnd = start + spaces.length;

            updateEditorLineNumbers();
        }
    });

    // Initialize line numbers on page load
    updateEditorLineNumbers();

    // Disable full-fix button until needed
    if (fullFixBtn) {
        fullFixBtn.disabled = true;
        fullFixBtn.title = "Disabled until analysis finds errors";
    }

    // Button actions
    if (runBtn) runBtn.addEventListener('click', explainCode);
    if (fullFixBtn) fullFixBtn.addEventListener("click", fullFixHandler);

    // Ctrl+Enter triggers analysis
    if (codeInput) {
        codeInput.placeholder = "paste your code here...";

        codeInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') explainCode();
        });

        // Auto-save typing to SQLite (debounced)
        let saveTimeout;
        codeInput.addEventListener("input", () => {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(saveCodeToDB, 800);
        });
    }

    // ================================
    // COPY BUTTONS
    // ================================
    const copyEditorBtn = document.getElementById("copyEditorBtn");
    const copyOutputBtn = document.getElementById("copyOutputBtn");

    if (copyEditorBtn) {
        copyEditorBtn.addEventListener("click", () => {
            const code = document.getElementById("codeInput")?.value || "";
            navigator.clipboard.writeText(code);
            showCopyToast("Code copied from editor!");
        });
    }

    if (copyOutputBtn) {
        copyOutputBtn.addEventListener("click", () => {
            const wrong = document.getElementById("wrongCode")?.innerText || "";
            const correct = document.getElementById("correctCode")?.innerText || "";
            const results = document.getElementById("results")?.innerText || "";

            // Combine everything the user might want to copy
            const finalText = (correct + "\n" + wrong + "\n" + results).trim();

            if (!finalText) {
                showCopyToast("Nothing to copy!", true);
                return;
            }

            navigator.clipboard.writeText(finalText);
            showCopyToast("Output copied!");
        });
    }

    // ================================
    // AI CHAT ASSISTANT
    // ================================
    const assistantBtn = document.getElementById("assistantBtn");
    const assistantInput = document.getElementById("assistantInput");
    const chatBox = document.getElementById("chatBox");

    if (assistantBtn) {
        assistantBtn.addEventListener("click", async () => {

            const message = assistantInput.value.trim();
            if (!message) return;

            // Add user message to chat
            appendMessage(message, "user");
            assistantInput.value = "";

            // Temporary loading message
            appendMessage("Thinking...", "assistant-temp");

            try {
                const res = await fetch("/assistant", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message })
                });

                const data = await res.json();

                // Remove temporary "thinking..." bubble
                const tempNode = chatBox.querySelector(".assistant-temp");
                if (tempNode) tempNode.remove();

                if (data.status === "success") {
                    appendMessage(data.reply, "assistant");
                } else {
                    appendMessage("⚠ Error: Unable to get response.", "assistant");
                }

            } catch (err) {
                // Remove temp message
                const tempNode = chatBox.querySelector(".assistant-temp");
                if (tempNode) tempNode.remove();

                appendMessage("⚠ Network error.", "assistant");
                console.error(err);
            }
        });
    }

    // Load saved data from DB
    loadSavedChat();
    loadLastSavedCode();
    loadProjects();
});


function normalizeLanguage(lang) {
    const map = {
        "cpp": "cpp",
        "c": "c",
        "csharp": "csharp",
        "java": "java",
        "javascript": "javascript",
        "typescript": "typescript",
        "python": "python",
        "go": "go",
        "rust": "rust",
        "r": "r",
        "php": "php",
        "perl": "perl",
        "ruby": "ruby",
        "swift": "swift",
        "kotlin": "kotlin",
        "dart": "dart",
        "matlab": "matlab",
        "sql": "sql",
        "html": "html",
        "css": "css",
        "elixir": "elixir",
        
    };

    return map[lang] || lang; // fallback safe
}


// ================================
// Main Analysis API Handler
// ================================
async function explainCode() {

    const code = document.getElementById('codeInput').value;
    const language = normalizeLanguage(
    document.getElementById('languageSelect').value);


    // various UI elements
    const outputDiv = document.getElementById('results');
    const wrongCodeDiv = document.getElementById('wrongCode');
    const correctCodeDiv = document.getElementById('correctCode');
    const loading = document.getElementById('loading');
    const fullFixBtn = document.getElementById('fullFixBtn');

    // Ensure user typed something
    if (!code.trim()) {
        outputDiv.innerHTML = `<div class="error-msg">⚠ Please enter some code to analyze.</div>`;
        fullFixBtn.disabled = true;
        return;
    }

    // Reset UI
    outputDiv.innerHTML = '';
    wrongCodeDiv.innerHTML = '';
    correctCodeDiv.innerHTML = '';
    loading.classList.remove('hidden');

    try {
        // Post code to backend
        const response = await fetch('/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();
        loading.classList.add('hidden');

        fullFixBtn.disabled = true;

        // Backend says wrong language
        if (data.status === 'language_mismatch') {
            outputDiv.innerHTML = `
                <div class="warning-msg">
                    <h3>⚠ Language Mismatch</h3>
                    <p>${data.message}</p>
                </div>`;
            return;
        }

        // Code has errors
        if (data.status === 'error') {

            fullFixBtn.disabled = false;
            fullFixBtn.title = "Click to generate full corrected code";

            let html = `
                <h3 style="color: var(--danger);">⚠ Issues Found</h3>
                <table class="error-table">
                    <thead>
                        <tr><th>Line</th><th>Issue</th><th>Details</th></tr>
                    </thead>
                    <tbody>`;

            // List each error returned by backend
            data.analysis.forEach(item => {
                html += `
                    <tr>
                        <td>${item.line}</td>
                        <td>${escapeHtml(item.issue)}</td>
                        <td>${escapeHtml(item.detail)}</td>
                    </tr>`;
            });

            html += `</tbody></table>`;
            outputDiv.innerHTML = html;
            return;
        }

        // Code is correct
        if (data.status === 'success') {
            fullFixBtn.disabled = true;
            renderSuccess(data, outputDiv);
            return;
        }

        // Fallback for unexpected response
        outputDiv.innerHTML =
            `<pre class="code-box">${escapeHtml(JSON.stringify(data, null, 2))}</pre>`;

    } catch (err) {
        loading.classList.add('hidden');
        fullFixBtn.disabled = true;
        outputDiv.innerHTML = `<div class="error-msg">Connection Error</div>`;
        console.error(err);
    }
}


// ================================
// Request Full Corrected Code
// ================================
async function fullFixHandler() {

    const code = document.getElementById("codeInput").value.trim();
    const language = document.getElementById("languageSelect").value;

    const loading = document.getElementById("loading");
    if (!code) return;

    loading.classList.remove("hidden");

    // Reset output UI
    document.getElementById("wrongCode").innerHTML = "";
    document.getElementById("correctCode").innerHTML = "";
    document.getElementById("results").innerHTML = "";

    try {
        const response = await fetch("/explain", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, language, mode: "full_fix" })
        });

        const data = await response.json();

        if (data.status === "full_fix_not_allowed") {
            document.getElementById("correctCode").innerHTML = `
                <div class="warning-msg">
                    <h3>⛔ Full Fix Not Allowed</h3>
                    <p>${escapeHtml(data.message)}</p>
                </div>`;
            loading.classList.add("hidden");
            return;
        }

        if (data.status === "language_mismatch") {
            document.getElementById("correctCode").innerHTML = `
                <div class="warning-msg">
                    <h3>⚠ Language Mismatch</h3>
                    <p>${escapeHtml(data.message)}</p>
                </div>`;
            loading.classList.add("hidden");
            return;
        }

        if (data.corrected_code) {
            document.getElementById("correctCode").innerHTML = `
                <div class="warning-msg" style="margin-bottom:12px;">
                    <strong>Note:</strong> ⚠ Fixed code can make mistakes. Please review it before use.
                </div>
                <h3>⚙ Fixed Code</h3>
                <div class="code-box">${escapeHtml(data.corrected_code)}</div>`;
            loading.classList.add("hidden");
            return;
        }

        document.getElementById("correctCode").innerHTML = `
            <div class="error-msg">❌ No corrected code returned.</div>`;
        loading.classList.add("hidden");

    } catch (err) {
        document.getElementById("results").innerHTML =
            `<div class="error-msg">Error generating full fix.</div>`;
        console.error(err);
        loading.classList.add("hidden");
    }
}


// ================================
// Renders success explanation cards
// ================================
function renderSuccess(data, container) {
    let html = '';
    if (data.intro) html += `<div class="mentor-intro">${data.intro}</div>`;

    html += `<div class="explanation-feed">`;

    data.analysis.forEach((item) => {
        html += `
        <div class="explain-card">
            <div class="card-header">
                <span class="line-badge">Line ${item.line}</span>
            </div>
            <div class="code-snippet">${escapeHtml(item.code)}</div>
            <div class="card-body">${item.description}</div>
        </div>`;
    });

    html += `</div>`;
    container.innerHTML = html;
}


// ================================
// Toast popup for copy actions
// ================================
function showCopyToast(text, isError = false) {
    const toast = document.createElement("div");
    toast.className = "copy-toast";
    toast.style.background = isError ? "#da3633" : "#238636";
    toast.innerText = text;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 250);
    }, 2000);
}


// Escape HTML before injecting into DOM
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// Append user or assistant message to chat
function appendMessage(text, sender) {
    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;

    const div = document.createElement("div");
    div.className =
        sender === "user" ? "msg user" :
        sender === "assistant" ? "msg assistant" :
        "msg assistant-temp";

    div.innerHTML = escapeHtml(text);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}


// Chat panel toggle
const chatButton = document.getElementById("chatButton");
const chatPanel = document.getElementById("chatPanel");

if (chatButton) {
    chatButton.addEventListener("click", () => {
        chatPanel.style.display =
            chatPanel.style.display === "flex" ? "none" : "flex";
    });
}


// Cleans markup from AI response before showing it
function cleanAIText(text) {
    if (!text) return "";
    return text
        .replace(/```[\s\S]*?```/g, "")
        .replace(/```/g, "")
        .replace(/`/g, "")
        .replace(/\*\*/g, "")
        .replace(/\\n/g, "\n")
        .trim();
}
const _appendMessage = appendMessage;

window.appendMessage = function(text, sender) {
    if (sender === "assistant") {
        text = cleanAIText(text);
    }
    _appendMessage(text, sender);
};

// ================================
// SQLite saving (frontend calls API)
// ================================
async function saveCodeToDB() {
    const code = document.getElementById("codeInput").value.trim();
    const language = document.getElementById("languageSelect").value;

    if (!code) return;

    try {
        await fetch("/save-code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, language })
        });
    } catch (err) {
        console.error("Auto-save failed", err);
    }
}


// Load last saved code
async function loadLastSavedCode() {
    try {
        const res = await fetch("/load-last-code");
        const data = await res.json();

        if (data.status === "success" && data.data) {
            const codeInput = document.getElementById("codeInput");
            codeInput.value = data.data.code;
            document.getElementById("languageSelect").value = data.data.language;
            
            // --- FIX START ---
            // Trigger an input event so line numbers update after the data loads
            codeInput.dispatchEvent(new Event('input'));
            // --- FIX END ---
        }
    } catch (err) {
        console.error("Error loading last code", err);
    }
}


// Load past chat messages
async function loadSavedChat() {
    try {
        const res = await fetch("/load-chat");
        const data = await res.json();

        if (data.status === "success") {
            data.chat.forEach(msg => {
                appendMessage(msg.user_message, "user");
                appendMessage(msg.ai_response, "assistant");
            });
        }
    } catch (err) {
        console.error("Chat load failed", err);
    }
}


// Prompt user to name a project and save it
async function saveProject() {
    const name = prompt("Enter project name:");
    if (!name) return;

    const code = document.getElementById("codeInput").value.trim();
    const language = document.getElementById("languageSelect").value;

    const res = await fetch("/save-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ projectName: name, code, language })
    });

    const data = await res.json();

    if (data.status === "success") {
        showCopyToast("Project saved!");
        loadProjects();
    }
}


// Load all saved projects
async function loadProjects() {
    const list = document.getElementById("projectList");
    if (!list) return;

    try {
        const res = await fetch("/projects");
        const data = await res.json();

        list.innerHTML = "";

        // Render each project in the sidebar
        data.projects.forEach(p => {
            list.innerHTML += `
                <div class="project-item">
                    <strong>${p.project_name}</strong>
                    <button onclick="loadProject(${p.id})">Load</button>
                    <button onclick="favoriteProject(${p.id}, ${p.is_favorite ? 0 : 1})">
                        ${p.is_favorite ? "★ Unfavorite" : "☆ Favorite"}
                    </button>
                    <button onclick="deleteProject(${p.id})">Delete</button>
                </div>`;
        });

    } catch (err) {
        console.error("Error loading projects", err);
    }
}


// Load a specific project into editor
async function loadProject(id) {
    const res = await fetch("/projects");
    const data = await res.json();

    const project = data.projects.find(p => p.id === id);
    if (!project) return;

    document.getElementById("codeInput").value = project.code;
    document.getElementById("languageSelect").value = project.language;
}


// Mark/unmark project as favorite
async function favoriteProject(id, fav) {
    await fetch("/favorite-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, fav })
    });

    loadProjects();
}


// Delete project
async function deleteProject(id) {
    await fetch("/delete-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });

    loadProjects();
}


// Simple reusable function to toggle floating panels
function togglePanel(buttonId, panelId) {
    const btn = document.getElementById(buttonId);
    const panel = document.getElementById(panelId);

    btn.addEventListener("click", () => {
        panel.style.display =
            panel.style.display === "flex" ? "none" : "flex";
    });
}

// Enable project sidebar toggle
togglePanel("projectsButton", "projectsPanel");

// ================================
// DARK MODE TOGGLE SYSTEM
// ================================

// Apply saved theme on page load
(function applySavedTheme() {
    const saved = localStorage.getItem("dark-mode");

    if (saved === "enabled") {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }
})();

// Toggle Dark/Light Mode
function toggleDarkMode() {
    const enabled = document.body.classList.toggle("dark-mode");
    localStorage.setItem("dark-mode", enabled ? "enabled" : "disabled");
}

// Attach toggle button
const darkModeBtn = document.getElementById("darkModeBtn");
if (darkModeBtn) {
    darkModeBtn.addEventListener("click", toggleDarkMode);
} 