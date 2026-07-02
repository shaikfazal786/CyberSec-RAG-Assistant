const askForm = document.getElementById("question-form");
const statusMessage = document.getElementById("status");
const answerCard = document.getElementById("answer-card");
const answerField = document.getElementById("answer");

function getHistory() {
  try {
    return JSON.parse(localStorage.getItem("chatHistory") || "[]");
  } catch {
    return [];
  }
}

function saveHistory(entry) {
  const history = getHistory();
  history.unshift(entry);
  localStorage.setItem("chatHistory", JSON.stringify(history.slice(0, 20)));
}

function renderResponse(answer) {
  if (!answerCard || !answerField) {
    return;
  }

  answerField.textContent = answer;
  answerCard.classList.remove("hidden");
}

function setStatus(message, isError = false) {
  if (!statusMessage) {
    return;
  }
  statusMessage.textContent = message;
  statusMessage.style.color = isError ? "#fda4af" : "#38bdf8";
}

async function askQuestion(question) {
  setStatus("Searching...");
  answerCard?.classList.add("hidden");

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const text = await response.text();
    let data = {};

    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = { error: text };
      }
    }

    if (!response.ok) {
      throw new Error(data.error || "Unable to fetch answer.");
    }

    renderResponse(data.answer);
    saveHistory({ question, answer: data.answer });
    setStatus("Answer returned successfully.");
  } catch (error) {
    setStatus(error.message || "Request failed.", true);
  }
}

if (askForm) {
  askForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const questionField = document.getElementById("question");
    if (!questionField) {
      return;
    }

    const question = questionField.value.trim();
    if (!question) {
      setStatus("Please enter a question.", true);
      return;
    }

    askQuestion(question);
  });
}
