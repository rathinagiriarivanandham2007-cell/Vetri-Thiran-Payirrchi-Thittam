const form = document.getElementById("recommendForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  result.classList.remove("hidden");
  result.innerHTML = "<h2>Generating recommendations...</h2>";

  const payload = {
    budget: Number(document.getElementById("budget").value),
    category: document.getElementById("category").value,
    preference: document.getElementById("preference").value || "value for money",
    goal: document.getElementById("goal").value || "best choice within my budget"
  };

  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }

    let html = `<h2>${escapeHtml(data.summary || "Your Recommendations")}</h2>`;

    (data.recommendations || []).forEach(item => {
      html += `
        <div class="rec">
          <strong>${escapeHtml(item.name)}</strong>
          <div class="price">Estimated: ₹${Number(item.estimated_price || 0).toLocaleString("en-IN")}</div>
          <p>${escapeHtml(item.reason || "")}</p>
        </div>`;
    });

    if (data.tips?.length) {
      html += "<h3>Smart Tips</h3><ul>";
      data.tips.forEach(tip => html += `<li>${escapeHtml(tip)}</li>`);
      html += "</ul>";
    }

    html += `<small>Recommendation source: ${escapeHtml(data.source || "AI")}</small>`;
    result.innerHTML = html;
  } catch (error) {
    result.innerHTML = `<h2>Something went wrong</h2><p>${escapeHtml(error.message)}</p>`;
  }
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
