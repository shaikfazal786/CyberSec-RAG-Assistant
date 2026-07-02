const historyList = document.getElementById("history-list");
const clearButton = document.getElementById("clear-history");

function getHistoryEntries() {
  try {
    return JSON.parse(localStorage.getItem("chatHistory") || "[]");
  } catch {
    return [];
  }
}

function renderHistory() {
  if (!historyList) {
    return;
  }

  const entries = getHistoryEntries();
  if (entries.length === 0) {
    historyList.innerHTML = "<li>No history available yet. Ask a question on the chat page.</li>";
    return;
  }

  historyList.innerHTML = entries
    .map(
      (entry, index) =>
        `<li><div class="history-item"><strong>${index + 1}. ${entry.question}</strong><p>${entry.answer}</p></div></li>`
    )
    .join("");
}

if (clearButton) {
  clearButton.addEventListener("click", () => {
    localStorage.removeItem("chatHistory");
    renderHistory();
  });
}

document.addEventListener("DOMContentLoaded", renderHistory);
