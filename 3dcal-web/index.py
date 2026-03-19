from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Configurações simples
CONFIG = {
    "printers": {
        "A1": {"name": "A1", "power_kw": 0.12},
        "P2S": {"name": "P2S", "power_kw": 0.15}
    },
    "costs": {
        "energy_per_kwh": 0.90,
        "wear_per_hour": 2.00,
        "failure_rate": 10.0,
        "maintenance_rate": 10.0
    },
    "investment": {
        "machine_value": 10000.0,
        "useful_life_years": 5.0,
        "hours_per_day": 8.0,
        "days_per_month": 30.0,
        "months_to_pay": 24.0
    }
}

def calculate_costs(printer_key, weight_g, filament_price_per_kg, time_h, profit_pct, quantity=1):
    printer = CONFIG["printers"][printer_key]
    costs = CONFIG["costs"]
    invest = CONFIG["investment"]
    
    material_cost = (weight_g / 1000) * filament_price_per_kg
    energy_cost = printer["power_kw"] * time_h * costs["energy_per_kwh"]
    wear_cost = time_h * costs["wear_per_hour"]
    failure_cost = (material_cost + energy_cost + wear_cost) * (costs["failure_rate"] / 100)
    maintenance_cost = (material_cost + energy_cost + wear_cost) * (costs["maintenance_rate"] / 100)
    depreciation_per_hour = invest["machine_value"] / (invest["useful_life_years"] * 365 * 24)
    depreciation_cost = time_h * depreciation_per_hour
    roi_per_hour = invest["machine_value"] / (invest["months_to_pay"] * invest["days_per_month"] * invest["hours_per_day"])
    roi_cost = time_h * roi_per_hour
    
    total_cost_per_piece = material_cost + energy_cost + wear_cost + failure_cost + maintenance_cost + depreciation_cost + roi_cost
    total_cost = total_cost_per_piece * quantity
    profit_amount = total_cost * (profit_pct / 100)
    sale_price = total_cost + profit_amount
    price_per_piece = sale_price / quantity
    
    return {
        "costs": {
            "material": round(material_cost, 2),
            "energy": round(energy_cost, 2),
            "wear": round(wear_cost, 2),
            "failure": round(failure_cost, 2),
            "maintenance": round(maintenance_cost, 2),
            "depreciation": round(depreciation_cost, 2),
            "roi": round(roi_cost, 2),
            "total_per_piece": round(total_cost_per_piece, 2)
        },
        "results": {
            "total_cost": round(total_cost, 2),
            "sale_price": round(sale_price, 2),
            "price_per_piece": round(price_per_piece, 2),
            "profit_amount": round(profit_amount, 2),
            "profit_percentage": round(profit_pct, 1)
        },
        "quantity": quantity
    }

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>3dcal - Calculadora 3D</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white p-8">
        <h1 class="text-4xl font-bold text-green-400 mb-8">3dcal - Calculadora de Impressões 3D</h1>
        
        <div class="max-w-4xl mx-auto">
            <div class="bg-gray-800 rounded-lg p-6 mb-6">
                <h2 class="text-xl font-bold mb-4">Configurações</h2>
                
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div>
                        <label class="block text-sm mb-2">Peso (g)</label>
                        <input type="number" id="weight" class="w-full p-2 bg-gray-700 rounded" placeholder="0.0">
                    </div>
                    <div>
                        <label class="block text-sm mb-2">Filamento (R$/kg)</label>
                        <input type="number" id="filament-price" class="w-full p-2 bg-gray-700 rounded" placeholder="0.0">
                    </div>
                    <div>
                        <label class="block text-sm mb-2">Tempo (h)</label>
                        <input type="number" id="time" class="w-full p-2 bg-gray-700 rounded" placeholder="0.0">
                    </div>
                    <div>
                        <label class="block text-sm mb-2">Lucro (%)</label>
                        <input type="number" id="profit" class="w-full p-2 bg-gray-700 rounded" placeholder="0.0">
                    </div>
                </div>
                
                <button onclick="calculate()" class="bg-green-500 text-black px-6 py-2 rounded font-bold hover:bg-green-400">
                    Calcular
                </button>
            </div>
            
            <div class="bg-gray-800 rounded-lg p-6">
                <h2 class="text-xl font-bold mb-4">Resultado</h2>
                <div class="text-3xl font-bold text-green-400" id="result">R$ 0,00</div>
            </div>
        </div>
        
        <script>
            async function calculate() {
                const weight = parseFloat(document.getElementById('weight').value) || 0;
                const filamentPrice = parseFloat(document.getElementById('filament-price').value) || 0;
                const time = parseFloat(document.getElementById('time').value) || 0;
                const profit = parseFloat(document.getElementById('profit').value) || 0;
                
                try {
                    const response = await fetch('/api/calculate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            printer: 'A1',
                            weight,
                            filament_price: filamentPrice,
                            time,
                            profit,
                            quantity: 1
                        })
                    });
                    
                    const result = await response.json();
                    document.getElementById('result').textContent = 'R$ ' + result.results.sale_price.toFixed(2).replace('.', ',');
                } catch (error) {
                    alert('Erro: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        printer = data.get('printer', 'A1')
        weight = float(data.get('weight', 0))
        filament_price = float(data.get('filament_price', 0))
        time = float(data.get('time', 0))
        profit = float(data.get('profit', 0))
        quantity = int(data.get('quantity', 1))
        
        result = calculate_costs(printer, weight, filament_price, time, profit, quantity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Vercel entrypoint
handler = app
