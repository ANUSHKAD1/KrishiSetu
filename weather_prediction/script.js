const cropDatabase = {
    Tomato: { 
        rules: { maxTemp: 35, minTemp: 10, rainLimit: 50 }, 
        recommendations: [
            "<strong>Maintain Soil Moisture Consistently:</strong> The forecast indicates potential dry spells. Tomatoes are highly susceptible to blossom-end rot and fruit cracking if their water supply is inconsistent. Aim for deep, regular watering that keeps the soil moist but not waterlogged. Check the soil a few inches down; if it's dry, it's time to water.",
            "<strong>Mitigate Heat Stress:</strong> Temperatures forecasted above 35°C can cause flowers to drop before pollination, drastically reducing your yield. If possible, deploy shade cloths during the peak heat of the day (11 AM - 4 PM) to protect the plants.",
            "<strong>Ensure Field Drainage Before Rain:</strong> The forecast predicts heavy rainfall. Tomatoes are prone to root rot and fungal diseases in waterlogged soil. Proactively check and clear drainage channels to ensure excess water can run off quickly."
        ] 
    },
    Cotton: { 
        rules: { maxTemp: 40, minTemp: 15, rainLimit: 60 }, 
        recommendations: [
            "<strong>Optimize Irrigation for Boll Development:</strong> The upcoming weather is critical for the boll development stage. Both over-watering and under-watering can cause the plant to shed its bolls. Adjust your irrigation schedule based on the rain forecast to maintain optimal soil moisture.",
            "<strong>Prepare for Potential Frost:</strong> Even a light frost can be fatal to young cotton plants. If nighttime temperatures are predicted to drop near the minimum threshold, be prepared with frost cloths or covers for smaller fields.",
            "<strong>Increase Pest Scouting in High Humidity:</strong> The forecast shows rising humidity, which creates a perfect breeding ground for pests like bollworms and aphids. Increase your field scouting frequency to catch any infestations early."
        ] 
    },
    Rice: { 
        rules: { maxTemp: 38, minTemp: 20, rainLimit: 80 }, 
        recommendations: [
            "<strong>Manage Paddy Water Levels:</strong> Rice requires consistently flooded fields, especially during the tillering and panicle initiation stages. Based on the rain forecast, regulate the inflow and outflow of water to maintain the ideal depth.",
            "<strong>Assess Lodging Risk:</strong> The forecast includes periods of heavy rain and potential wind. Tall, heavy-headed rice varieties are at risk of lodging (falling over). If your crop is in its late stages, consider draining the field slightly to help the soil anchor the plants more firmly.",
            "<strong>Guard Against Cold Shock:</strong> Temperatures forecasted below 20°C during the flowering stage can lead to pollen sterility and a poor grain set. If this is a risk, maintaining a slightly deeper water level in the paddy can help insulate the plants overnight."
        ] 
    },
    Wheat: { 
        rules: { maxTemp: 30, minTemp: 5, rainLimit: 40 }, 
        recommendations: [
            "<strong>Critical Irrigation for Grain Fill:</strong> The forecast suggests dry periods ahead. The 'grain fill' stage is when the plant pumps nutrients into the kernel, and water stress now will result in shriveled, low-quality grain. Ensure deep soil moisture is available.",
            "<strong>Monitor for Late Frost During Flowering:</strong> A frost during the delicate flowering stage can destroy the pollen and prevent fertilization, resulting in empty heads. This is a high-impact risk that must be monitored closely.",
            "<strong>Evaluate Heat Stress Impact:</strong> The forecast shows temperatures approaching 30°C. Extreme heat during the grain-filling period can prematurely shut down the plant's development, leading to lower yields. Ensure the crop is not stressed for water, which helps it regulate temperature."
        ] 
    },
    Maize: { // Corn
        rules: { maxTemp: 33, minTemp: 10, rainLimit: 60 },
        recommendations: [
            "<strong>Prioritize Water at Tasseling/Silking:</strong> This is the most critical period for maize. The forecast indicates potential water stress. Drought during pollination can cause incomplete kernel set and is the leading cause of yield loss. Do not skip irrigation cycles during this phase.",
            "<strong>Assess Wind and Rain Lodging Risk:</strong> Tall maize with a heavy ear is like a sail in the wind. The combination of saturated soil from the forecasted rain and high winds can lead to widespread lodging. Check field drainage to ensure soil is not overly soft.",
            "<strong>Anticipate Pollination Issues in Extreme Heat:</strong> Temperatures above 33°C can dry out the silks before they can be pollinated by the tassels. If extreme heat is predicted, irrigating beforehand can raise local humidity and help maintain silk viability."
        ]
    },
    Sugarcane: {
        rules: { maxTemp: 38, minTemp: 20, rainLimit: 70 },
        recommendations: [
            "<strong>Plan for High Water Demand:</strong> Sugarcane has a long growing season and requires significant water. The upcoming forecast suggests a need for supplemental irrigation to support vigorous cane growth and sucrose accumulation.",
            "<strong>Frost is a Critical Threat:</strong> Frost can rupture the plant's cells and cause the stored sucrose to begin degrading immediately, ruining the quality of your crop for processing. If frost is a possibility, harvesting susceptible fields should be prioritized.",
            "<strong>Ensure Soil is Not Waterlogged:</strong> While it's a thirsty crop, sugarcane's root system can be damaged by standing water for extended periods. The forecast calls for heavy rain, so ensure your drainage systems are clear and functional to prevent root rot."
        ]
    }
};

document.getElementById("getForecast").addEventListener("click", async () => {
    const location = document.getElementById("location").value;
    const crop = document.getElementById("crop").value;
    if (!location) { alert("Please enter a location"); return; }

    try {
        const geoResponse = await fetch("api/geocode", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ location })
        });
        const geoData = await geoResponse.json();
        if (geoData.error) { alert(geoData.error); return; }

        const { lat, lng } = geoData;
        const weatherResponse = await fetch("api/weather", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lat, lng })
        });
        
        if (!weatherResponse.ok) {
            const errorData = await weatherResponse.json();
            throw new Error(errorData.error || `HTTP error! status: ${weatherResponse.status}`);
        }

        const weatherData = await weatherResponse.json();
        if (weatherData.error) { alert(weatherData.error); return; }

        displayResults(weatherData, crop);

    } catch (err) {
        console.error(err);
        alert("Failed to fetch weather data: " + err.message);
    }
});

function displayResults(weatherData, crop) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.classList.remove("hidden");

    const dailyData = processForecastList(weatherData.list);
    const daily = Object.values(dailyData);
    const cropRules = cropDatabase[crop].rules;

    let status = "Safe";
    for (let day of daily) {
        if (day.max_temp > cropRules.maxTemp || day.min_temp < cropRules.minTemp || (day.rain || 0) > cropRules.rainLimit) {
            status = "Warning";
        }
    }
    
    const statusCard = document.getElementById("statusCard");
    statusCard.textContent = `Status: ${status}`;
    if(status === "Safe") statusCard.style.backgroundColor = "#2ecc71"; // Green
    if(status === "Warning") statusCard.style.backgroundColor = "#f39c12"; // Orange

    const labels = daily.map(d => d.date);
    const temps = daily.map(d => d.avg_temp);
    const ctx = document.getElementById("forecastChart").getContext("2d");
    if (window.myChart) window.myChart.destroy();
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: { 
            labels, 
            datasets: [{ 
                label: 'Average Daily Temperature (°C)', 
                data: temps, 
                borderColor: '#030d76ff', 
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                fill: true,
                tension: 0.4
            }] 
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    const dailyList = document.getElementById("dailyForecast");
    dailyList.innerHTML = ""; // Clear previous list
    for (let day of daily) {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${day.date}:</strong> <span>${day.description}, Temp: ${day.min_temp.toFixed(1)}°C - ${day.max_temp.toFixed(1)}°C, Rain: ${day.rain.toFixed(2)}mm</span>`;
        dailyList.appendChild(li);
    }

    const recList = document.getElementById("recommendations");
    recList.innerHTML = ""; // Clear previous list
    cropDatabase[crop].recommendations.forEach(rec => {
        const li = document.createElement("li");
        li.innerHTML = rec; // Use innerHTML to render the <strong> tags
        recList.appendChild(li);
    });
}

function processForecastList(list) {
    const dailyData = {};

    list.forEach(item => {
        const date = new Date(item.dt * 1000).toLocaleDateString();
        if (!dailyData[date]) {
            dailyData[date] = {
                date: date,
                temps: [],
                min_temp: item.main.temp_min,
                max_temp: item.main.temp_max,
                rain: 0,
                description: item.weather[0].description
            };
        }
        
        dailyData[date].temps.push(item.main.temp);
        dailyData[date].min_temp = Math.min(dailyData[date].min_temp, item.main.temp_min);
        dailyData[date].max_temp = Math.max(dailyData[date].max_temp, item.main.temp_max);
        if (item.rain && item.rain['3h']) {
            dailyData[date].rain += item.rain['3h'];
        }
    });

    for (const date in dailyData) {
        const sum = dailyData[date].temps.reduce((a, b) => a + b, 0);
        dailyData[date].avg_temp = sum / dailyData[date].temps.length;
    }

    return dailyData;
}