document.getElementById("cropForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  const data = {
    N: parseFloat(document.getElementById("N").value),
    P: parseFloat(document.getElementById("P").value),
    K: parseFloat(document.getElementById("K").value),
    temperature: parseFloat(document.getElementById("temperature").value),
    humidity: parseFloat(document.getElementById("humidity").value),
    ph: parseFloat(document.getElementById("ph").value),
    rainfall: parseFloat(document.getElementById("rainfall").value)
  };

  const response = await fetch("/predict", {  // same port as Flask
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  const result = await response.json();
  document.getElementById("result").innerHTML = 
    `<b>Recommended Crop:</b> 🌾 ${result.recommended_crop}`;
});
