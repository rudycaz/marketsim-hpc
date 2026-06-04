document.getElementById("forecast-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const output = document.getElementById("output");
  output.textContent = "Running forecast...";

  const payload = {
    ticker: document.getElementById("ticker").value,
    horizon: document.getElementById("horizon").value,
    simulations: Number(document.getElementById("simulations").value),
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/forecast", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    output.textContent = `Error: ${error.message}`;
  }
});
