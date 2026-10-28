
const chatBody = document.getElementById("chatBody");
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");

const chatPage = document.getElementById("chatPage");
const historyPage = document.getElementById("historyPage");
const historyList = document.getElementById("historyList");
const historyCount = document.getElementById("historyCount");
const breadcrumbTitle = document.getElementById("breadcrumbTitle");

const STORAGE_KEY = "smart_academic_history_v1";

let messages = [];
let busy = false;

function loadHistory() {
    try {
        const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        return Array.isArray(data) ? data : [];
    } catch {
        return [];
    }
}

function saveHistory(history) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

function createMessage(role, content, id = "") {
    const row = document.createElement("div");
    row.className = `message ${role === "user" ? "user-message" : ""}`;
    if (id) row.id = id;

    if (role === "assistant") {
        const avatar = document.createElement("div");
        avatar.className = "bot-mini";
        const icon = document.createElement("i");
        icon.className = "fa-solid fa-robot";
        avatar.appendChild(icon);
        row.appendChild(avatar);
    }

    const contentBox = document.createElement("div");
    contentBox.className = "message-content";

    const name = document.createElement("div");
    name.className = "message-name";
    name.textContent = role === "user" ? "Kamu" : "Academic Assistant";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = content;

    contentBox.append(name, bubble);
    row.appendChild(contentBox);
    return row;
}

function scrollToBottom() {
    chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: "smooth"
    });
}

function renderMessages() {
    chatBody.querySelectorAll(".message").forEach(el => el.remove());

    const welcome = document.getElementById("welcomeMessage");
    const popular = document.getElementById("popularQuestions");

    welcome.hidden = messages.length > 0;
    popular.hidden = messages.length > 0;

    messages.forEach(message => {
        chatBody.appendChild(createMessage(message.role, message.content));
    });

    scrollToBottom();
}

function newConversation() {
    messages = [];
    renderMessages();
    questionInput.value = "";
    questionInput.focus();
    history.pushState({}, "", "/");
}

async function sendQuestion(question) {
    question = question.trim();

    if (!question || busy) return;

    busy = true;
    sendButton.disabled = true;
    questionInput.disabled = true;

    const welcome = document.getElementById("welcomeMessage");
    const popular = document.getElementById("popularQuestions");
    welcome.hidden = true;
    popular.hidden = true;

    messages.push({ role: "user", content: question });
    chatBody.appendChild(createMessage("user", question));
    questionInput.value = "";

    const loading = createMessage("assistant", "Sedang mencari informasi akademik...");
    loading.classList.add("loading-message");
    chatBody.appendChild(loading);
    scrollToBottom();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: question })
        });

        const data = await response.json();

        loading.remove();

        if (!response.ok) {
            throw new Error(data.error || "Gagal mendapatkan jawaban.");
        }

        const answer = String(data.answer || "Maaf, jawaban belum tersedia.");

        messages.push({ role: "assistant", content: answer });
        chatBody.appendChild(createMessage("assistant", answer));

        // Simpan percakapan ke localStorage
        const historyData = loadHistory();
        historyData.unshift({
            id: `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
            question,
            answer,
            date: new Date().toISOString()
        });

        saveHistory(historyData.slice(0, 100));
    } catch (error) {
        loading.remove();

        const message = error.message || "Terjadi kesalahan saat menghubungi server.";
        messages.push({ role: "assistant", content: message });
        chatBody.appendChild(createMessage("assistant", message));
    } finally {
        busy = false;
        sendButton.disabled = false;
        questionInput.disabled = false;
        questionInput.focus();
        scrollToBottom();
    }
}

function formatDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "Tanggal tidak tersedia";

    return date.toLocaleString("id-ID", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function openHistoryItem(item) {
    messages = [
        { role: "user", content: item.question },
        { role: "assistant", content: item.answer }
    ];

    chatPage.hidden = false;
    historyPage.hidden = true;
    breadcrumbTitle.textContent = "Chat Assistant";

    history.pushState({}, "", "/");
    renderMessages();
}

function renderHistory() {
    const data = loadHistory();
    historyCount.textContent = data.length;
    historyList.replaceChildren();

    if (data.length === 0) {
        const empty = document.createElement("div");
        empty.className = "history-empty";

        const icon = document.createElement("div");
        icon.className = "empty-icon";
        icon.innerHTML = '<i class="fa-regular fa-comments"></i>';

        const title = document.createElement("h3");
        title.textContent = "Belum Ada Riwayat";

        const description = document.createElement("p");
        description.textContent = "Percakapan yang kamu lakukan akan muncul di sini.";

        const button = document.createElement("a");
        button.className = "primary-button";
        button.href = "/";
        button.innerHTML = '<i class="fa-solid fa-plus"></i> Mulai Percakapan';

        empty.append(icon, title, description, button);
        historyList.appendChild(empty);
        return;
    }

    data.forEach(item => {
        const card = document.createElement("article");
        card.className = "history-card";

        const icon = document.createElement("div");
        icon.className = "history-card-icon";
        icon.innerHTML = '<i class="fa-regular fa-comments"></i>';

        const info = document.createElement("div");
        info.className = "history-card-info";

        const title = document.createElement("h3");
        title.textContent = item.question;

        const answer = document.createElement("p");
        answer.textContent = item.answer;

        const date = document.createElement("span");
        date.innerHTML = '<i class="fa-regular fa-clock"></i> ';
        date.appendChild(document.createTextNode(formatDate(item.date)));

        info.append(title, answer, date);

        const actions = document.createElement("div");
        actions.className = "history-card-actions";

        const openButton = document.createElement("button");
        openButton.className = "open-history-button";
        openButton.innerHTML = '<i class="fa-solid fa-arrow-up-right-from-square"></i> Buka';
        openButton.addEventListener("click", () => openHistoryItem(item));

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-history-button";
        deleteButton.setAttribute("aria-label", "Hapus percakapan");
        deleteButton.innerHTML = '<i class="fa-regular fa-trash-can"></i>';
        deleteButton.addEventListener("click", () => {
            if (!confirm("Hapus percakapan ini?")) return;
            saveHistory(loadHistory().filter(entry => entry.id !== item.id));
            renderHistory();
        });

        actions.append(openButton, deleteButton);
        card.append(icon, info, actions);
        historyList.appendChild(card);
    });
}

function showPage(page) {
    const isHistory = page === "history";

    chatPage.hidden = isHistory;
    historyPage.hidden = !isHistory;
    breadcrumbTitle.textContent = isHistory ? "History" : "Chat Assistant";

    document.querySelectorAll(".navigation .menu-item").forEach(link => {
        link.classList.remove("active");
    });

    document.getElementById(isHistory ? "historyNav" : "historyNav")
        .classList.toggle("active", isHistory);

    if (!isHistory) {
        document.querySelector('.navigation .menu-item[href="/"]')
            ?.classList.add("active");
    } else {
        renderHistory();
    }

    history.pushState({ page }, "", isHistory ? "/?page=history" : "/");
}

chatForm.addEventListener("submit", event => {
    event.preventDefault();
    sendQuestion(questionInput.value);
});

document.querySelectorAll("[data-question]").forEach(button => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});

document.getElementById("newChat").addEventListener("click", newConversation);

document.getElementById("historyNav").addEventListener("click", event => {
    event.preventDefault();
    showPage("history");
});

document.getElementById("clearHistory").addEventListener("click", () => {
    if (!loadHistory().length) return;
    if (!confirm("Yakin ingin menghapus semua riwayat percakapan?")) return;

    saveHistory([]);
    renderHistory();
});

window.addEventListener("popstate", () => {
    const page = new URLSearchParams(location.search).get("page");
    chatPage.hidden = page === "history";
    historyPage.hidden = page !== "history";
    breadcrumbTitle.textContent = page === "history" ? "History" : "Chat Assistant";
    if (page === "history") renderHistory();
});

const initialPage = new URLSearchParams(location.search).get("page");
if (initialPage === "history") {
    chatPage.hidden = true;
    historyPage.hidden = false;
    breadcrumbTitle.textContent = "History";
    renderHistory();
}

renderMessages();
