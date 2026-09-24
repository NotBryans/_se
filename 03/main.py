import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="SmartFit Macro Calculator")


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SmartFit Macro Calculator</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
            .container { max-width: 480px; background: #1e293b; margin: 20px auto; padding: 24px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155; }
            h2 { color: #38bdf8; text-align: center; margin-top: 0; font-size: 22px; }
            label { display: block; margin-top: 14px; font-size: 14px; color: #94a3b8; font-weight: 600; }
            input, select { width: 100%; padding: 10px; margin-top: 6px; background: #0f172a; color: #fff; border: 1px solid #475569; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
            input:focus, select:focus { outline: none; border-color: #38bdf8; }
            button { width: 100%; margin-top: 22px; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
            button:hover { background: #0369a1; }
            .result { margin-top: 20px; padding: 16px; background: #0f172a; border-radius: 8px; border-left: 4px solid #38bdf8; display: none; }
            .result h3 { margin-top: 0; color: #38bdf8; font-size: 18px; }
            .metric { display: flex; justify-content: space-between; margin: 8px 0; font-size: 14px; }
            hr { border: 0; border-top: 1px solid #334155; margin: 12px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💪 SmartFit Tracker & Calculator</h2>
            
            <label>Gender</label>
            <select id="gender">
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>

            <label>Age</label>
            <input type="number" id="age" value="20">

            <label>Height (cm)</label>
            <input type="number" id="height" value="175">

            <label>Weight (kg)</label>
            <input type="number" id="weight" value="70">

            <label>Goal</label>
            <select id="goal">
                <option value="maintain">Maintain Weight</option>
                <option value="cut">Fat Loss (-20% Cal)</option>
                <option value="bulk">Muscle Gain (+15% Cal)</option>
            </select>

            <button onclick="calculate()">Calculate Macros</button>

            <div id="result" class="result">
                <h3>Your Daily Plan</h3>
                <div class="metric"><span>BMR:</span> <strong id="bmr"></strong> kcal</div>
                <div class="metric"><span>TDEE:</span> <strong id="tdee"></strong> kcal</div>
                <div class="metric"><span>Target Calories:</span> <strong id="targetCalories"></strong> kcal</div>
                <hr>
                <div class="metric"><span>Protein:</span> <strong id="protein"></strong> g</div>
                <div class="metric"><span>Fat:</span> <strong id="fat"></strong> g</div>
                <div class="metric"><span>Carbs:</span> <strong id="carbs"></strong> g</div>
            </div>
        </div>

        <script>
            function calculate() {
                const gender = document.getElementById('gender').value;
                const age = parseFloat(document.getElementById('age').value);
                const height = parseFloat(document.getElementById('height').value);
                const weight = parseFloat(document.getElementById('weight').value);
                const goal = document.getElementById('goal').value;

                let bmr = (10 * weight) + (6.25 * height) - (5 * age);
                bmr += (gender === 'male') ? 5 : -161;

                let tdee = bmr * 1.55;

                let targetCalories = tdee;
                if (goal === 'cut') targetCalories *= 0.8;
                if (goal === 'bulk') targetCalories *= 1.15;

                const proteinGrams = weight * 2.0;
                const fatGrams = (targetCalories * 0.25) / 9;
                const carbsGrams = (targetCalories - (proteinGrams * 4) - (fatGrams * 9)) / 4;

                document.getElementById('bmr').innerText = Math.round(bmr);
                document.getElementById('tdee').innerText = Math.round(tdee);
                document.getElementById('targetCalories').innerText = Math.round(targetCalories);
                document.getElementById('protein').innerText = Math.round(proteinGrams);
                document.getElementById('fat').innerText = Math.round(fatGrams);
                document.getElementById('carbs').innerText = Math.round(carbsGrams);

                document.getElementById('result').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)