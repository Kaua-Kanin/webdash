async function loadCrypto() {
  const tbody = document.querySelector("#crypto-table tbody");
  tbody.innerHTML = "<tr><td colspan='3'>Carregando...</td></tr>";
  try {
    const res = await fetch("/api/crypto");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Erro ao carregar dados.");
    tbody.innerHTML = data.map((coin) => `
      <tr>
        <td>${coin.name}</td>
        <td>${coin.usd != null ? "$" + coin.usd.toLocaleString() : "-"}</td>
        <td>${coin.brl != null ? "R$" + coin.brl.toLocaleString() : "-"}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="3">${err.message}</td></tr>`;
  }
}

document.getElementById("weather-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = document.getElementById("city-input").value.trim();
  const resultEl = document.getElementById("weather-result");
  resultEl.textContent = "Buscando...";
  try {
    const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Erro ao buscar clima.");
    resultEl.innerHTML = `
      <p><strong>${data.city}, ${data.country}</strong></p>
      <p>${data.temperature_c}&deg;C — Umidade ${data.humidity_pct}% — Vento ${data.wind_kmh} km/h</p>
    `;
  } catch (err) {
    resultEl.textContent = err.message;
  }
});

loadCrypto();
