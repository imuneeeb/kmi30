from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Stock data - Updated based on KMI30 rebalancing
sectors_data = {
    "Oil and Gas Exploration Companies": ["MARI", "PPL", "OGDC"],
    "Cement": ["FCCL", "MLCF", "DGKC", "LUCK"],  # Removed PIOS
    "Commercial Banks": ["MEBL"],  # Removed FABL
    "INV. Banks/INV. COS/Securities Cos": ["ENGROH"],
    "Power Generation and Distribution": ["HUBC", "CNERGICO"],  # Added CNERGICO
    "Technology and Communication": ["SYS", "AIRLINK"],  # Removed NETSOL, AVN, OCTOPUS; Added AIRLINK
    "Oil and Gas Marketing Companies": ["SNGP", "PSO", "SSGC"],  # Added SSGC
    "Fertilizers": ["EFERT", "FFC"],  # Added FFC
    "Automobile Assembler": ["SAZEW", "MTL", "GAL", "GHNI"],  # Removed HCAR
    "Refinery": ["ATRL", "PRL", "NRL"],  # Added NRL
    "Cable and Electrical Goods": ["PAEL"],
    "Pharmaceuticals": ["SEARL", "GSK", "CITI"],  # Added GSK, CITI
    "Food and Personal Care Products": ["FFL", "TOMCL"]  # Removed TOMCL (The Organic Meat Company)
}

company_names = {
    "MARI": "Mari Petroleum Company Limited",
    "PPL": "Pakistan Petroleum Limited",
    "OGDC": "Oil and Gas Development Company Limited",
    "FCCL": "Fauji Cement Company Limited",
    "MLCF": "Maple Leaf Cement Factory Limited",
    "DGKC": "D. G. Khan Cement Company Limited",
    "LUCK": "Lucky Cement Limited",
    "MEBL": "Meezan Bank Limited",
    "ENGROH": "Engro Corporation Limited",
    "HUBC": "Hub Power Company Limited",
    "CNERGICO": "Cnergico PK Limited",
    "SYS": "Systems Limited",
    "AIRLINK": "Air Link Communication Limited",
    "SNGP": "Sui Northern Gas Pipelines Limited",
    "PSO": "Pakistan State Oil Company Limited",
    "SSGC": "Sui Southern Gas Company Limited",
    "EFERT": "Engro Fertilizers Limited",
    "FFC": "Fauji Fertilizer Company Limited",
    "SAZEW": "Sazgar Engineering Works Limited",
    "MTL": "Millat Tractors Limited",
    "GAL": "Ghandhara Automobile Limited",
    "GHNI": "Ghandhara Nissan Limited",
    "ATRL": "Attock Refinery Limited",
    "PRL": "Pakistan Refinery Limited",
    "NRL": "National Refinery Limited",
    "PAEL": "Pakistan Cables Limited",
    "SEARL": "The Searle Company Limited",
    "GSK": "GlaxoSmithKline Pakistan",
    "CITI": "Citi Pharma Limited",
    "FFL": "Fauji Foods Limited",
    "TOMCL": "Tomato Pakistan Limited"
}

company_weights = {
    # Existing companies - keep their weights
    "ENGROH": 10.14, "LUCK": 9.3, "HUBC": 9.29, "MEBL": 9.15, "MARI": 8.06,
    "OGDC": 7.64, "SYS": 6.22, "EFERT": 6.19, "PPL": 6.18, "PSO": 4.88,
    "MLCF": 2.39, "DGKC": 2.38, "MTL": 2.22, "FCCL": 2.22,
    "SAZEW": 1.76, "SNGP": 1.59, "ATRL": 1.38, "PAEL": 1.29,
    "SEARL": 1.26, "GAL": 0.6, "GHNI": 0.57, "FFL": 0.45, "PRL": 0.39,
    "TOMCL": 0.25,
    # New incoming companies - weights not disclosed yet
    "SSGC": 0, "FFC": 0, "GSK": 0, "NRL": 0, "AIRLINK": 0, "CITI": 0, "CNERGICO": 0
}

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/sectors')
def sectors():
    return render_template('sectors.html')

@app.route('/api/stocks')
def get_stocks():
    stocks = []
    for sector, companies in sectors_data.items():
        for company in companies:
            stocks.append({
                'sector': sector,
                'symbol': company,
                'name': company_names.get(company, f"{company} Limited"),
                'weight': company_weights.get(company, 0)
            })
    return jsonify(stocks)

if __name__ == '__main__':
    import os
    import sys
    
    # Run on 0.0.0.0:443 with HTTPS by default (accessible from network and localhost)
    host = '0.0.0.0'  # This allows both localhost and network access
    port = 443
    ssl_context = 'adhoc'  # Self-signed certificate
    
    # Allow HTTP mode for development
    if '--http' in sys.argv:
        port = 8000  # Use port 8000 to avoid macOS AirPlay conflict
        ssl_context = None
        print("Running in HTTP mode on port 8000")
        print("Accessible at:")
        print("  - http://localhost:8000")
        print("  - http://127.0.0.1:8000")
        print("  - http://0.0.0.0:8000")
    else:
        print("Running with HTTPS on port 443")
        print("Note: Requires sudo and pyOpenSSL")
    
    port = int(os.environ.get('PORT', port))
    
    app.run(debug=False, host=host, port=port, ssl_context=ssl_context)
