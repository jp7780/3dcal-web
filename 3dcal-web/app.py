from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

# Configurações da calculadora
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
    """Calcula custos e preço final"""
    printer = CONFIG["printers"][printer_key]
    costs = CONFIG["costs"]
    invest = CONFIG["investment"]
    
    # Custo material
    material_cost = (weight_g / 1000) * filament_price_per_kg
    
    # Custo energia
    energy_cost = printer["power_kw"] * time_h * costs["energy_per_kwh"]
    
    # Custo desgaste
    wear_cost = time_h * costs["wear_per_hour"]
    
    # Custo falhas (% adicional)
    failure_cost = (material_cost + energy_cost + wear_cost) * (costs["failure_rate"] / 100)
    
    # Custo manutenção (% adicional)
    maintenance_cost = (material_cost + energy_cost + wear_cost) * (costs["maintenance_rate"] / 100)
    
    # Depreciação por hora
    depreciation_per_hour = invest["machine_value"] / (invest["useful_life_years"] * 365 * 24)
    depreciation_cost = time_h * depreciation_per_hour
    
    # ROI por hora
    roi_per_hour = invest["machine_value"] / (invest["months_to_pay"] * invest["days_per_month"] * invest["hours_per_day"])
    roi_cost = time_h * roi_per_hour
    
    # Custo total por peça
    total_cost_per_piece = material_cost + energy_cost + wear_cost + failure_cost + maintenance_cost + depreciation_cost + roi_cost
    
    # Custo total
    total_cost = total_cost_per_piece * quantity
    
    # Preço de venda
    profit_amount = total_cost * (profit_pct / 100)
    sale_price = total_cost + profit_amount
    
    # Preço por peça
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
    return render_template('index.html', config=CONFIG)

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

if __name__ == '__main__':
    app.run(debug=True)
