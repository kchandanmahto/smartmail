
const API = "/api";

const emailInput = document.getElementById("emailInput");
const tone = document.getElementById("tone");
const length = document.getElementById("length");
const generateBtn = document.getElementById("generateBtn");

const resultSection = document.getElementById("resultSection");
const historySection = document.getElementById("historySection");
const workspace = document.getElementById("workspace");

function showMessage(message) {
    const element = document.getElementById("message");

    element.textContent = message;
    element.style.display = "block";

    setTimeout(() => {
        element.style.display = "none";
    }, 3000);
}

function showWorkspace() {
    workspace.hidden = false;
    historySection.hidden = true;
    document.getElementById("historyNav").classList.remove("active");
    document.getElementById("homeNav").classList.add("active");
}

function showHistoryView() {
    workspace.hidden = true;
    historySection.hidden = false;
    document.getElementById("homeNav").classList.remove("active");
    document.getElementById("historyNav").classList.add("active");

    loadHistory();
}

function renderResult(data) {
    const analysis = data.analysis;

    document.getElementById("summary").textContent =
        analysis.summary;

    document.getElementById("intent").textContent =
        analysis.intent;

    document.getElementById("category").textContent =
        analysis.category;

    document.getElementById("sentiment").textContent =
        analysis.sentiment;

    document.getElementById("priority").textContent =
        analysis.priority;

    const keyPoints = document.getElementById("keyPoints");

    keyPoints.replaceChildren();

    analysis.key_points.forEach(point => {
        const li = document.createElement("li");
        li.textContent = point;
        keyPoints.appendChild(li);
    });

    document.getElementById("replyOutput").value =
        data.reply;

    resultSection.hidden = false;

    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

generateBtn.addEventListener("click", async () => {

    const email = emailInput.value.trim();

    if (email.length < 10) {
        showMessage("Please enter a valid email.");
        return;
    }

    generateBtn.disabled = true;
    generateBtn.textContent = "Analyzing Email...";

    try {
        const response = await fetch(`${API}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                tone: tone.value,
                length: length.value
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Something went wrong"
            );
        }

        renderResult(result.data);
        showMessage("AI reply generated successfully!");

    } catch (error) {
        showMessage(error.message);

    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "✦ Generate AI Reply";
    }
});


document.getElementById("copyBtn").addEventListener(
    "click",
    async () => {
        const reply = document.getElementById("replyOutput").value;

        try {
            await navigator.clipboard.writeText(reply);
            showMessage("Reply copied!");
        } catch {
            showMessage("Clipboard access failed.");
        }
    }
);


async function loadHistory() {

    const historyList = document.getElementById("historyList");

    historyList.replaceChildren();

    try {
        const response = await fetch(`${API}/history`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to load history");
        }

        if (result.data.length === 0) {
            const empty = document.createElement("p");
            empty.textContent = "No email history found.";
            historyList.appendChild(empty);
            return;
        }

        result.data.forEach(item => {

            const card = document.createElement("div");
            card.className = "history-item";

            const heading = document.createElement("strong");
            heading.textContent =
                `#${item.id} · ${item.analysis.category}`;

            const description = document.createElement("p");
            description.textContent =
                item.email.slice(0, 140);

            const meta = document.createElement("p");
            meta.textContent =
                `Priority: ${item.analysis.priority} · ${new Date(item.created_at).toLocaleString()}`;

            card.append(heading, description, meta);

            card.addEventListener("click", () => {
                renderResult(item);
                showWorkspace();
            });

            historyList.appendChild(card);
        });

    } catch (error) {
        showMessage(error.message);
    }
}


document.getElementById("historyNav").addEventListener(
    "click",
    showHistoryView
);

document.getElementById("homeNav").addEventListener(
    "click",
    showWorkspace
);

document.getElementById("newEmail").addEventListener(
    "click",
    () => {
        showWorkspace();
        emailInput.value = "";
        resultSection.hidden = true;
        emailInput.focus();
    }
);

document.getElementById("refreshHistory").addEventListener(
    "click",
    loadHistory
);
