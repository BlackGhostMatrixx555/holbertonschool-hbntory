// Point d'entrée du Service IA (Task 5). À adapter à l'URL réelle une fois
// déployé (ou à charger depuis une config/env si vous préférez).
const AI_SERVICE_URL = "http://localhost:8002/api/v1/query";

const form = document.getElementById("query-form");
const input = document.getElementById("question-input");
const submitBtn = document.getElementById("submit-btn");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  await askQuestion(question);
});

document.querySelectorAll(".example-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    input.value = btn.textContent;
    askQuestion(btn.textContent);
  });
});

async function askQuestion(question) {
  setLoading(true);
  try {
    const response = await fetch(AI_SERVICE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`Service responded with status ${response.status}`);
    }

    const data = await response.json();
    showAnswer(data.answer);
  } catch (err) {
    showError(
      "The assistant is currently unavailable. Please try again in a moment."
    );
    console.error("AI Query Service error:", err);
  } finally {
    setLoading(false);
  }
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  if (isLoading) {
    result.innerHTML = `<p class="result-loading">Thinking…</p>`;
  }
}

function showAnswer(answer) {
  result.innerHTML = `<p class="result-answer"></p>`;
  result.querySelector(".result-answer").textContent = answer;
}

function showError(message) {
  result.innerHTML = `<p class="result-error"></p>`;
  result.querySelector(".result-error").textContent = message;
}
