const suggestions = [
  "What is phishing?",
  "How does ransomware work?",
  "Explain MITRE ATT&CK.",
  "What is incident response?",
  "What is social engineering?",
];

function renderSuggestions() {
  const list = document.getElementById("suggestion-list");
  if (!list) {
    return;
  }

  list.innerHTML = suggestions
    .map((question) => `<li><button class="suggestion-button" type="button">${question}</button></li>`)
    .join("");

  list.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      const questionField = document.getElementById("question");
      if (questionField) {
        questionField.value = button.textContent || "";
        questionField.focus();
      }
    });
  });
}

function setActivePage() {
  const page = document.body.dataset.page;
  const navLinks = document.querySelectorAll(".site-nav .nav-link");
  navLinks.forEach((link) => {
    if (link.getAttribute("href") === window.location.pathname) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderSuggestions();
  setActivePage();
});
