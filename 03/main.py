```python
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="SmartFit Macro Calculator")


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SmartFit 智慧營養試算器</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; }
            .container { max-width: 500px; background: white; margin: 30px auto; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h2 { color: #2c3e50; text-align: center; margin-bottom: 20px; }
            label { display: block; margin-top: 12px; font-weight: bold; color: #34495e; }
            input, select { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
            button { width: 100%; margin-top: 20px; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
            button:hover { background: #219150; }
            .result { margin-top: 20px; padding: 15px; background: #e8f8f5; border-radius: 6px; border-left: 5px solid #27ae60; display: none; }
            .result h3 { margin-top: 0; color: #16a085; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💪 SmartFit 營養素試算器</h2>
            
            <label>性別</label>
            <select id="gender">
                <option value="male">男性</option>
                <option value="female">女性</option>
            </select>

            <label>年齡</label>
            <input type="number" id="age" value="20">

            <label>身高 (cm)</label>
            <input type="number" id="height" value="175">

            <label>體重 (kg)</label>
            <input type="number" id="weight" value="70">

            <label>目標</label>
            <select id="goal">
                <option value="maintain">維持體重</option>
                <option value="cut">減脂 (-20% 熱量)</option>
                <option value="bulk">增肌 (+15% 熱量)</option>
            </select>

            <button onclick="calculate()">一鍵計算每日目標</button>

            <div id="result" class="result">
                <h3>試算結果</h3>
                <p><strong>BMR (基礎代謝):</strong> <span id="bmr"></span> kcal</p>
                <p><strong>TDEE (每日總消耗):</strong> <span id="tdee"></span> kcal</p>
                <p><strong>目標每日熱量:</strong> <span id="targetCalories"></span> kcal</p>
                <hr>
                <p><strong>蛋白质 (Protein):</strong> <span id="protein"></span> g</p>
                <p><strong>脂肪 (Fat):</strong> <span id="fat"></span> g</p>
                <p><strong>碳水化合物 (Carbs):</strong> <span id="carbs"></span> g</p>
            </div>
        </div>

        <script>
            function calculate() {
                const gender = document.getElementById('gender').value;
                const age = parseFloat(document.getElementById('age').value);
                const height = parseFloat(document.getElementById('height').value);
                const weight = parseFloat(document.getElementById('weight').value);
                const goal = document.getElementById('goal').value;

                // Mifflin-St Jeor Formula
                let bmr = (10 * weight) + (6.25 * height) - (5 * age);
                bmr += (gender === 'male') ? 5 : -161;

                let tdee = bmr * 1.55; // Moderate activity factor

                let targetCalories = tdee;
                if (goal === 'cut') targetCalories *= 0.8;
                if (goal === 'bulk') targetCalories *= 1.15;

                // Macros Calculation
                const proteinGrams = weight * 2.0; // 2g per kg
                const fatGrams = (targetCalories * 0.25) / 9; // 25% calories from fat
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